from typing import Any

from .interfaces import ISavable, IUsernameKeySavable


class AbstractField:
    def __init__(self, name, t:type, allowed_none:bool=False) -> None:
        self._NAME: str = name
        self._TYPE: type = t
        self._ALLOWED_NONE = allowed_none
        self._value = None

        if not isinstance(name, str):
            raise TypeError(type(name))
        if not isinstance(t, type):
            raise TypeError(type(t))
        if not isinstance(allowed_none, bool):
            raise TypeError(type(allowed_none))
        
    @property
    def NAME(self) -> str:
        return self._NAME
    
    @property
    def TYPE(self) -> type:
        return self._TYPE
    
    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, v:Any) -> None:
        if not isinstance(v, self._TYPE):
            if self._ALLOWED_NONE and not v is None: 
                raise TypeError(f'{type(v)}, expected: {self._TYPE}')
        self._value = v

    def getValueFromObject(self, object:Any) -> None:
        raise NotImplementedError()

    def setValueToObject(self, object:Any) -> None:
        raise NotImplementedError()

class IdField(AbstractField):
    def __init__(self) -> None:
        super().__init__('id', int)

    def getValueFromObject(self, object:ISavable) -> None:
        self._value = object.id 

    def setValueToObject(self, object:ISavable) -> None:
        object.id = self._value

class UsernameField(AbstractField):
    def __init__(self) -> None:
        super().__init__('username', str)

    def getValueFromObject(self, object:IUsernameKeySavable) -> None:
        self._value = object.username

    def setValueToObject(self, object:IUsernameKeySavable) -> None:
        object.username = self._value
        
