from typing import Tuple, List, Any, Dict

from .fields import AbstractField
from .type_converters import *


class DatabaseSaverLoader:
    def __init__(self) -> None:
        self._FIELDS = None
        self._SUPPORTED_TYPES = (int, float, str, bytes, type(None))
        self._type_converters: List[AbstractDBTypeConverter] = [
            BoolDBTypeConverter(),
            DatetimeDBTypeConverter(),
            DateDBTypeConverter(),
            ListDBTypeConverter(),
            TupleDBTypeConverter(),
            DictDBTypeConverter()
        ]
    
    @property
    def FIELDS(self) -> Tuple[AbstractField]:
        return self._FIELDS
    
    @FIELDS.setter
    def FIELDS(self, value:Tuple[AbstractField]) -> None:
        if not isinstance(value, tuple):
            raise TypeError(type(value))
        self._FIELDS = value

    def setTypeConverters(self, converters:Tuple[AbstractDBTypeConverter], replace:bool=False) -> None:
        if replace:
            self._type_converters = list(converters)
        else:
            self._type_converters += list(converters)

    def getParamsAndValues(self, object:Any) -> Tuple[Tuple[str], Tuple[Any]]:
        params_list: List[str] = []
        values_list: List[Any] = []
        for field in self._FIELDS:
            field.getValueFromObject(object)
            params_list.append(field.NAME)
            values_list.append(self._getFieldValue(field))
        
        return tuple(params_list), tuple(values_list)
    
    def setValuesToObject(self, object:Any, values:Tuple[Any]) -> None:
        if len(self._FIELDS) != len(values):
            raise ValueError(len(self._FIELDS), len(values))
        
        data: Dict[AbstractField, Any] = dict(zip(self._FIELDS, values))

        for field in data.keys():
            self._setFieldValue(field, data[field])
            field.setValueToObject(object)

    def _getFieldValue(self, field:AbstractField) -> Any:
        value = field.value
        if not type(value) in self._SUPPORTED_TYPES:
            for converter in self._type_converters:
                if isinstance(value, converter.TYPE):
                    value = converter.toDatabase(value)
                    break
            else:
                raise TypeError(type(value))

        return value

    def _setFieldValue(self, field:AbstractField, value) -> None:
        if value is None:
            if not field._ALLOWED_NONE:
                raise ValueError(f'Field "{field.NAME}" not allowed None type')
            field.value = None
        else:
            if not field.TYPE in self._SUPPORTED_TYPES:
                for converter in self._type_converters:
                    if converter.TYPE == field.TYPE:
                        value = converter.fromDatabase(value)
                        break
                else:
                    raise TypeError(field.TYPE)
            
            field.value = value


