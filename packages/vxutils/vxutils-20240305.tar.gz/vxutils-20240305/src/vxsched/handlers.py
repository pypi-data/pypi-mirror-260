"""事件处理器模块"""

import logging
from collections import defaultdict
from typing import Dict, List, Callable, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, Executor, as_completed, Future
from vxsched.event import VXEvent
from vxutils import VXContext, VXDatetime


class VXSubscriber:
    """事件处理器"""

    __subscribers__: Dict[str, "VXSubscriber"] = {}
    __executor__: Executor = ThreadPoolExecutor(thread_name_prefix="VXSubscriber")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._callbacks: Dict[str, List[Callable[[VXContext, VXEvent], Any]]] = (
            defaultdict(list)
        )

    @property
    def callbacks(
        self,
    ) -> Dict[str, List[Callable[[VXContext, VXEvent], Any]]]:
        return self._callbacks

    def subscribe(
        self,
        event_type: str,
        callback: Callable[[VXContext, VXEvent], Any],
    ) -> None:
        """注册事件处理器"""
        if callback not in self._callbacks[event_type]:
            self._callbacks[event_type].append(callback)
            logging.debug(
                f"{self.__class__.__name__} id({id(self)}) Register event handler: {event_type} -> {callback}"
            )

    def unsubscribe(self, event_type: str, callback: Callable[..., Any]) -> None:
        """注销事件处理器"""
        if callback in self._callbacks[event_type]:
            self._callbacks[event_type].remove(callback)
            logging.debug(
                f"{self.__class__.__name__} id({id(self)}) Unregister event handler: {event_type} -> {callback}"
            )

    def __call__(
        self, event_type: str
    ) -> Callable[
        [Callable[[VXContext, VXEvent], Any]], Callable[[VXContext, VXEvent], Any]
    ]:
        """事件调度"""

        def decorator(callback: Callable[[VXContext, VXEvent], Any]) -> Any:
            self.subscribe(event_type, callback)
            return callback

        return decorator

    def execute(self, context: VXContext, event: VXEvent) -> Any:
        """事件处理"""
        fns = []
        for callback in self._callbacks[event.type]:
            fn = self.__executor__.submit(callback, context, event)
            callback_event = VXEvent(
                type="on_done_callback",
                data={"callback": callback, "context": context, "event": event},
                channel="__subscribers__",
            )
            fn.add_done_callback(lambda x: self.on_done_callback(x, callback_event))
            fns.append(fn)
        return list(as_completed(fns))

    def on_done_callback(self, fn: Future[Any], event: VXEvent) -> Any:
        """错误处理"""
        cost = VXDatetime.now() - event.created_dt
        if cost > 1:
            logging.warning(
                f"Event({event.data['event'].type})  cost: {cost*1000:,.3f}ms.",
                exc_info=True,
                stack_info=True,
            )
        return fn.result()

    def merge(self, other: "VXSubscriber") -> "VXSubscriber":
        """合并事件处理器"""
        for event_type, callbacks in other.callbacks.items():
            for callback in callbacks:
                if callback not in self._callbacks[event_type]:
                    self._callbacks[event_type].append(callback)
                    logging.debug(
                        "Merge event handler: %s -> %s", event_type, callbacks
                    )
        return self


if __name__ == "__main__":
    import time
    from vxutils import loggerConfig

    loggerConfig("DEBUG")

    handlers = VXSubscriber()
    ctx = VXContext()

    def handler1(context: VXContext, event: VXEvent) -> None:
        print(f"handler1: {event.type}")
        time.sleep(0.1)
        # raise ValueError("test")

    handlers.subscribe("event1", handler1)
    start = time.perf_counter()
    handlers.execute(ctx, VXEvent(type="event1"))
    logging.info(f"Time: {time.perf_counter() - start}")
