"""事件处理器模块"""

import logging
from collections import defaultdict
from typing import Dict, List, Callable, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, Executor, as_completed, Future
from vxsched.event import VXEvent
from vxutils import VXContext, VXDatetime


class VXHandlers:
    __executor__: Executor = ThreadPoolExecutor(thread_name_prefix="Handlers")

    def __init__(self, is_async: bool = True) -> None:
        self._handlers: Dict[str, List[Callable[[VXContext, VXEvent], Any]]] = (
            defaultdict(list)
        )
        self._is_async = is_async

    @property
    def handlers(
        self,
    ) -> Dict[str, List[Callable[[VXContext, VXEvent], Any]]]:
        return self._handlers

    def register(
        self,
        event_type: str,
        handler: Callable[[VXContext, VXEvent], Any],
    ) -> None:
        """注册事件处理器"""
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)
            logging.debug(
                f"{self.__class__.__name__} id({id(self)}) Register event handler: {event_type} -> {handler}"
            )

    def unregister(self, event_type: str, handler: Callable[..., Any]) -> None:
        """注销事件处理器"""
        if handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)
            logging.debug(
                f"{self.__class__.__name__} id({id(self)}) Unregister event handler: {event_type} -> {handler}"
            )

    def __call__(
        self, event_type: str
    ) -> Callable[
        [Callable[[VXContext, VXEvent], Any]], Callable[[VXContext, VXEvent], Any]
    ]:
        """事件调度"""

        def decorator(handler: Callable[[VXContext, VXEvent], Any]) -> Any:
            self.register(event_type, handler)
            return handler

        return decorator

    def execute(self, context: VXContext, event: VXEvent) -> Any:
        """事件处理"""
        fns = []
        for handler in self._handlers[event.type]:
            fn = self.__executor__.submit(handler, context, event)
            callback_event = VXEvent(
                type="on_done_callback",
                data={"handler": handler, "context": context, "event": event},
                channel="__handlers__",
            )
            fn.add_done_callback(lambda x: self.on_done_callback(x, callback_event))
            fns.append(fn)
        return fns if self._is_async else list(as_completed(fns))

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

    def merge(self, other: "VXHandlers") -> "VXHandlers":
        """合并事件处理器"""
        for event_type, handlers in other.handlers.items():
            for handler in handlers:
                if handler not in self._handlers[event_type]:
                    self._handlers[event_type].append(handler)
                    logging.debug("Merge event handler: %s -> %s", event_type, handler)
        return self


if __name__ == "__main__":
    import time
    from vxutils import init_colored_console

    init_colored_console("DEBUG")

    handlers = VXHandlers()
    ctx = VXContext()

    def handler1(context: VXContext, event: VXEvent) -> None:
        print(f"handler1: {event.type}")
        time.sleep(0.1)
        # raise ValueError("test")

    handlers.register("event1", handler1)
    start = time.perf_counter()
    handlers.execute(ctx, VXEvent(type="event1"))
    logging.info(f"Time: {time.perf_counter() - start}")
