"""事件处理核心模块"""

import logging
from typing import List, Dict, Callable, Any, DefaultDict, Optional, Union
from contextlib import suppress
from queue import Empty

from vxsched.event import VXEvent, VXEventQueue, VXTrigger
from vxsched.handlers import VXHandlers
from vxutils import VXContext

ON_INIT_EVENT = "__init__"
ON_REPLY_EVENT = "__reply__"
ON_TASK_COMPLETE_EVENT = "__task_complete__"
ON_EXIT_EVENT = "__exit__"


class VXScheduler:
    """事件调度器"""

    def __init__(
        self,
        context: Optional[Union[Dict[str, Any], VXContext]] = None,
        *,
        handlers: Optional[VXHandlers] = None,
    ) -> None:
        if context is None:
            context = {}
        self._handlers: VXHandlers = handlers or VXHandlers()
        self._context: VXContext = VXContext(**context)
        self._queue: VXEventQueue = VXEventQueue()
        self._is_active: bool = False

    @property
    def handlers(self) -> VXHandlers:
        return self._handlers

    @property
    def context(self) -> VXContext:
        return self._context

    @property
    def is_active(self) -> bool:
        return self._is_active

    def run(self) -> None:
        """运行事件调度器"""

        try:
            self.start()
            while self.is_active:
                with suppress(Empty):
                    event = self._queue.get(timeout=1)
                    self.handlers.execute(self._context, event)
        finally:
            self.stop()

    def start(self) -> None:
        """启动事件调度器"""
        self._is_active = True
        self.handlers.execute(
            self._context, VXEvent(type=ON_INIT_EVENT, channel="__handlers__")
        )
        logging.info("Event scheduler started")

    def stop(self) -> None:
        """停止事件调度器"""
        self._is_active = False
        self.handlers.execute(
            self._context, VXEvent(type=ON_EXIT_EVENT, channel="__handlers__")
        )
        logging.info("Event scheduler stopped")

    def publish(
        self,
        event: Union[str, VXEvent],
        *,
        trigger: Optional[VXTrigger] = None,
        channel: str = "default",
    ) -> None:
        """发布事件"""
        if isinstance(event, str):
            event = VXEvent(type=event, channel=channel)
        self._queue.put(event, trigger=trigger)


if __name__ == "__main__":
    from vxutils import VXDatetime

    sched = VXScheduler()

    sched.handlers.register("test", lambda x, y: print(VXDatetime.now(), x, y))
    sched.publish(
        VXEvent(type="test", data={"test": "test"}),
        trigger=VXTrigger.every(3, start_dt=VXDatetime.today(timestr="09:30:00")),
    )
    sched.run()
