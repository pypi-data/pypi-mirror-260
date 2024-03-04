from .interfaces import ISavable
from .fields import AbstractField

class IDBRequest:
    def save(self, object:ISavable) -> None:
        raise NotImplementedError()
    
    def load(self, object:ISavable) -> bool:
        raise NotImplementedError()
    
    def update(self, object:ISavable) -> None:
        raise NotImplementedError()

    def delete(self, object:ISavable) -> None:
        raise NotImplementedError() 
    
    def loadAll(self, object_sample:ISavable, limit:int=None, reverse:bool=True, sortField:AbstractField=None) -> list:
        raise NotImplementedError()