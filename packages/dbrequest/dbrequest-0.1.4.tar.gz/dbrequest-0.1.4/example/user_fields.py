from dbrequest import AbstractField

from user import User


class UserUsernameField(AbstractField):
    def getValueFromObject(self, object:User) -> None:
        self._value = object.username 

    def setValueToObject(self, object:User) -> None:
        object.username = self._value

class UserLastMessageField(AbstractField):
    def getValueFromObject(self, object:User) -> None:
        self._value = object.lastMessage 

    def setValueToObject(self, object:User) -> None:
        object.lastMessage = self._value

        