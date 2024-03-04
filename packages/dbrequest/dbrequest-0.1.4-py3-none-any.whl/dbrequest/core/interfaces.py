class ISavable:
    @property
    def id(self) -> int:
        raise NotImplementedError()
    
    @id.setter
    def id(self, value) -> None:
        raise NotImplementedError()
    
class IUsernameKeySavable:
    @property
    def username(self) -> str:
        raise NotImplementedError()

    @username.setter
    def username(self, value) -> None:
        raise NotImplementedError()
    
class IJsonable:
    def toJson(self) -> str:
        raise NotImplementedError()
    
    def fromJson(self, json_str:str) -> None:
        raise NotImplementedError()
    
