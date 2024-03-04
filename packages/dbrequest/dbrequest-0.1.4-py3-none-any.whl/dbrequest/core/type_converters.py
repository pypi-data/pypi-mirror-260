from typing import Any
from datetime import datetime as Datetime, date as Date

import json 


class AbstractDBTypeConverter:
    def __init__(self) -> None:
        self._TYPE: type = None

    @property
    def TYPE(self) -> type:
        return self._TYPE

    def toDatabase(self, value:Any) -> Any:
        raise NotImplementedError()

    def fromDatabase(self, value:Any) -> Any:
        raise NotImplementedError()

# Default converters

class BoolDBTypeConverter(AbstractDBTypeConverter):
    def __init__(self) -> None:
        self._TYPE: type = bool

    def toDatabase(self, value: bool) -> int:
        return int(value)

    def fromDatabase(self, value: int) -> bool:
        return value == 1

class DatetimeDBTypeConverter(AbstractDBTypeConverter):
    def __init__(self) -> None:
        self._TYPE: type = Datetime

    def toDatabase(self, value: Datetime) -> int:
        timestamp = value.timestamp()
        if value.microsecond == 0:
            timestamp = int(timestamp)

        return timestamp

    def fromDatabase(self, value: int) -> Datetime:
        if not isinstance(value, int):
            raise TypeError(type(value))
        if value is not None:
            return Datetime.fromtimestamp(value)

class DateDBTypeConverter(AbstractDBTypeConverter):
    def __init__(self) -> None:
        self._TYPE: type = Date

    def toDatabase(self, value: Date) -> int:
        return value.toordinal()

    def fromDatabase(self, value: int) -> Date:
        if value is not None:
            return Date.fromordinal(value)

class AbstractJsonableDBTypeConverter(AbstractDBTypeConverter):
    def toDatabase(self, value: Any) -> str:
        return json.dumps(value)

    def fromDatabase(self, value: str) -> Any:
        if value is not None:
            return json.loads(value)
        
class ListDBTypeConverter(AbstractJsonableDBTypeConverter):
    def __init__(self) -> None:
        self._TYPE: type = list

class TupleDBTypeConverter(AbstractJsonableDBTypeConverter):
    def __init__(self) -> None:
        self._TYPE: type = tuple

class DictDBTypeConverter(AbstractJsonableDBTypeConverter):
    def __init__(self) -> None:
        self._TYPE: type = dict
