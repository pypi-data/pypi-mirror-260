# endcoding = utf-8
"""
author : vex1023
email :  vex1023@qq.com
各类型的decorator
"""


import time
import logging
import signal
from typing import Callable, Union, Tuple, Any, Type
from concurrent.futures import ThreadPoolExecutor, Future, Executor
from multiprocessing.pool import ThreadPool
from multiprocessing import Lock
from functools import wraps
from vxutils import __logger_root__

__all__ = [
    "retry",
    "timeit",
    "singleton",
    "timeout",
]
logger = logging.getLogger(f"{__logger_root__}.{__name__}")

###################################
# 错误重试方法实现
# @retry(tries, CatchExceptions=(Exception,), delay=0.01, backoff=2)
###################################


class retry:

    def __init__(
        self,
        tries: int,
        cache_exceptions: Union[Type[Exception], Tuple[Type[Exception]]],
        delay: float = 0.1,
        backoff: int = 2,
    ) -> None:
        """重试装饰器

        Arguments:
            tries {int} -- 重试次数
            cache_exceptions {Union[Exception, Tuple[Exception]]} -- 发生错误时，需要重试的异常列表

        Keyword Arguments:
            delay {float} -- 延时时间 (default: {0.1})
            backoff {int} -- 延时时间等待倍数 (default: {2})
        """
        if backoff <= 1:
            raise ValueError("backoff must be greater than 1")

        if tries < 0:
            raise ValueError("tries must be 0 or greater")

        if delay <= 0:
            raise ValueError("delay must be greater than 0")

        if not isinstance(cache_exceptions, (tuple, list)):
            cache_exceptions = (cache_exceptions,)

        self._tries = tries
        self._cache_exceptions = tuple(cache_exceptions)
        self._delay = delay
        self._backoff = backoff

    def __call__(self, func: Callable[[Any], Any]) -> Callable[[Any], Any]:

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            mdelay = self._delay
            for i in range(1, self._tries):
                try:
                    return func(*args, **kwargs)
                except self._cache_exceptions as err:
                    logger.error(
                        "function %s(%s, %s) try %s times error: %s\n",
                        func.__name__,
                        args,
                        kwargs,
                        i,
                        err,
                    )
                    logger.warning("Retrying in %.4f seconds...", mdelay)

                    time.sleep(mdelay)
                    mdelay *= self._backoff

            return func(*args, **kwargs)

        return wrapper


###################################
# 计算运行消耗时间
# @timeit
###################################


class timeit:
    """
    计算运行消耗时间
    @timeit
    def test():
        time.sleep(1)
    """

    def __init__(self, func: Callable[[Any], Any]) -> None:
        self._func = func

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        _start = time.perf_counter()
        retval = self._func(*args, **kwargs)
        _end = time.perf_counter()
        logger.info(
            "function %s(%s,%s) used : %f:.6fms",
            self._func.__name__,
            args,
            kwargs,
            (_end - _start) * 1000,
        )
        return retval


###################################
# Singleton 实现
# @singleton
###################################


class singleton(object):
    """
    单例
    example::

        @singleton
        class YourClass(object):
            def __init__(self, *args, **kwargs):
                pass
    """

    def __init__(self, cls: Type[Any]) -> None:
        self._instance = None
        self._cls = cls
        self._lock = Lock()

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    self._instance = self._cls(*args, **kwargs)
        return self._instance


###################################
# 限制超时时间
# @timeout(seconds, error_message='Function call timed out')
###################################


class TimeoutError(Exception):
    pass


class timeout:

    def __init__(
        self, seconds: float = 1, *, timeout_msg: str = "Function %s call time out."
    ) -> None:
        self._timeout = seconds
        self._timeout_msg = timeout_msg

        pass

    def __call__(self, func: Callable[[Any], Any]) -> Callable[[Any], Any]:

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            signal.signal(signal.SIGALRM, self._handle_timeout)
            signal.alarm(self._timeout)
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)

        return wrapper

    def _handle_timeout(self, signum: int, frame: Any) -> None:
        raise TimeoutError(
            f"{self._timeout_msg} after {self._timeout *1000}ms,{signum},{frame}"
        )
