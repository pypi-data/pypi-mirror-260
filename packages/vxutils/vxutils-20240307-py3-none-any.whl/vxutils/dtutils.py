"""日期工具"""

import time
from datetime import datetime, date, timedelta, tzinfo
from typing import Union, Optional, Generator, Any
from dateutil.parser import parse as dt_parse
from vxutils import Datetime, to_datetime


_min_timestamps = datetime(1980, 1, 1).timestamp()


class VXDatetime(datetime):
    """扩展 datetime 类"""

    __default_timefunc__ = time.time

    @classmethod
    def today(
        cls, tz: Optional[tzinfo] = None, *, timestr: str = "00:00:00"
    ) -> "VXDatetime":

        return cls.combine(date.today(), dt_parse(timestr).time(), tz)

    def __add__(self, __value: Union[timedelta, float, int]) -> "VXDatetime":
        if isinstance(__value, (float, int)):
            __value = timedelta(seconds=__value)
        return super().__add__(__value)

    def __radd__(self, __value: Union[timedelta, float, int]) -> "VXDatetime":
        if isinstance(__value, (float, int)):
            __value = timedelta(seconds=__value)
        return super().__radd__(__value)

    def __sub__(self, __value: Any) -> Any:
        if isinstance(__value, timedelta):
            return super().__sub__(__value)
        elif isinstance(__value, (float, int)) and __value < _min_timestamps:
            return super().__sub__(timedelta(seconds=__value))
        elif isinstance(__value, (datetime, date, time.struct_time, str, float, int)):
            __value = to_datetime(__value)
            delta = super().__sub__(__value)
            return delta.total_seconds()
        raise TypeError(f"不支持的类型: {type(__value)}")

    # *@overload
    # *def __sub__(
    # *    self, __value: Union[datetime, date, time.struct_time, str], /
    # *) -> timedelta: ...
    # *
    # *@overload
    # *def __sub__(self, __value: timedelta) -> "VXDatetime": ...
    # *
    # *@overload
    # *def __sub__(self, __value: Union[float, int]) -> Union["VXDatetime", timedelta]: ...

    def __rsub__(self, __value: Datetime) -> timedelta:
        __value = to_datetime(__value)
        return -self.__sub__(__value)

    @classmethod
    def from_pydatetime(cls, dt: Datetime) -> "VXDatetime":
        """从 datetime 类型转换

        Arguments:
            dt {Datetime} -- 待转换的日期

        Returns:
            VXDatetime -- 转换结果
        """
        if isinstance(dt, VXDatetime):
            return dt

        if isinstance(dt, (date, float, int, str, time.struct_time)):
            date_time: datetime = to_datetime(dt)
        elif isinstance(dt, (datetime)):
            date_time = dt
        else:
            raise ValueError(f"无法转换为 VXDatetime 类型: {dt}")

        return cls(
            year=date_time.year,
            month=date_time.month,
            day=date_time.day,
            hour=date_time.hour,
            minute=date_time.minute,
            second=date_time.second,
            microsecond=date_time.microsecond,
            tzinfo=date_time.tzinfo,
            fold=date_time.fold,
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, (time.struct_time, str, float, int)):
            __value = to_datetime(__value)
            return super().__eq__(__value)
        elif isinstance(__value, (datetime, date, VXDatetime)):
            return super().__eq__(__value)
        return False

    def __ge__(self, __value: Datetime) -> bool:
        __value = to_datetime(__value)
        return super().__ge__(__value)

    def __gt__(self, __value: Datetime) -> bool:
        __value = to_datetime(__value)
        return super().__gt__(__value)

    def __lt__(self, __value: Datetime) -> bool:
        __value = to_datetime(__value)
        return super().__lt__(__value)

    def __le__(self, __value: Datetime) -> bool:
        __value = to_datetime(__value)
        return super().__le__(__value)

    def __hash__(self) -> int:
        return super().__hash__()


VXDatetime.max: VXDatetime = VXDatetime.from_pydatetime(datetime.max)
VXDatetime.min: VXDatetime = VXDatetime.from_pydatetime(_min_timestamps)

# @classmethod
# def __get_pydantic_core_schema__(
#    cls, source: Type[Any], handler: GetCoreSchemaHandler
# ) -> core_schema.CoreSchema:
#    print(source, handler)
#    schema = handler(source)  # get the CoreSchema from the type / inner constraints
#    print(schema)
#    if schema["type"] != "str":
#        raise TypeError("RestrictCharacters can only be applied to strings")
#    return core_schema.no_info_after_validator_function(
#        to_vxdatetime,
#        schema,
#    )

# def validate(self, value: Datetime) -> "VXDatetime":
#    return to_vxdatetime(value)


def date_range(
    start: Datetime, end: Datetime, interval: Union[timedelta, float, int]
) -> Generator[VXDatetime, None, None]:
    """生成日期范围

    Arguments:
        start {PYDATETIME} -- 起始日期
        end {PYDATETIME} -- 结束日期
        interval {Union[timedelta, float, int]} -- 间隔

    Returns:
        list[VXDatetime] -- 日期范围
    """
    start = VXDatetime.from_pydatetime(start)
    end = VXDatetime.from_pydatetime(end)
    if start > end:
        raise ValueError("起始日期不能大于结束日期")
    ret = start
    while ret <= end:
        yield ret
        ret += interval


def to_vxdatetime(dt: Datetime) -> VXDatetime:
    """转换为 VXDatetime 类型

    Arguments:
        dt {Datetime} -- 待转换的日期

    Returns:
        VXDatetime -- 转换结果
    """
    return VXDatetime.from_pydatetime(dt)


if __name__ == "__main__":
    dt1 = VXDatetime(2023, 1, 2)
    print(dt1)
    print(VXDatetime.today(timestr="12:34:56") + 4)
    print(4 + VXDatetime.today(timestr="12:34:56"))
    print(VXDatetime.from_pydatetime("2023-01-02 12:34:56"))
    print(VXDatetime.from_pydatetime(1641107696.0))

    print(dt1 - 3)
    print(time.time() - dt1)
    dt2 = dt1.timestamp()
    print(dt1 == dt2)
    dt3 = dt1.date()
    print(dt1 == dt3)
    print(dt1 == str(dt1))
    print(dt1 > dt1 + 3)
    print("2023-01-02 12:34:56" > dt1 - 3)
    print(dt1.timestamp() > dt1 - 3)
    print(hash(dt1))
    print(hash(dt1 + 3))
    # for i in date_range("2023-01-01", "2023-01-3", 30 * 60):
    #    print(i)
    print(VXDatetime.now(), VXDatetime.now() + 1, VXDatetime.now() - 1)
