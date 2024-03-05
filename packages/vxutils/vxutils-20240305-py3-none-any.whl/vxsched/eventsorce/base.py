"""消息来源基类"""

from typing import Callable, Any
from vxutils.context import VXContext
from vxsched.event import VXEvent


class EventSourceBase:
    """消息来源基类"""

    def __init__(self, channel: str) -> None:
        self._channel = channel

    def start(self) -> None:
        """启动消息来源"""
        raise NotImplementedError

    def stop(self) -> None:
        """停止消息来源"""
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self._channel})"

    def __repr__(self) -> str:
        return self.__str__()

    def register(self, handler: Callable[[VXContext, VXEvent], Any]) -> None:
        """注册事件处理器"""
        raise NotImplementedError
