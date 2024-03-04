from dbrequest import Savable


class User(Savable):
    def __init__(self) -> None:
        super().__init__()
        self._username: str = None
        self._last_message: str = None

    @property
    def username(self) -> str:
        return self._username
    
    @property
    def lastMessage(self) -> str:
        return self._last_message

    @username.setter
    def username(self, value:str) -> None:
        if not isinstance(value, str):
            raise TypeError(type(value))
        if value == '':
            raise ValueError(value)
        self._username = value
    
    @lastMessage.setter
    def lastMessage(self, value:str) -> None:
        if not isinstance(value, str) and not value is None:
            raise TypeError(type(value))
        self._last_message = value

            