from typing import Dict

from .interfaces import ISavable
from .idb_request import IDBRequest
from .fields import AbstractField


class AbstractUniversalDBRequest(IDBRequest):
    def __init__(self) -> None:
        self._REQUESTS: Dict[ISavable, IDBRequest] = {}

    def save(self, object:ISavable) -> None:
        self._getStorageRequest(object).save(object)
    
    def load(self, object:ISavable) -> bool:
        return self._getStorageRequest(object).load(object)
    
    def update(self, object:ISavable) -> None:
        self._getStorageRequest(object).update(object)

    def delete(self, object:ISavable) -> None:
        self._getStorageRequest(object).delete(object)
    
    def loadAll(self, object_sample:ISavable, limit:int=None, reverse:bool=True, sortField:AbstractField=None) -> list:
        return self._getStorageRequest(object_sample).loadAll(object_sample, limit, reverse, sortField)
    
    def _getStorageRequest(self, object:ISavable) -> IDBRequest:
        return self._REQUESTS[type(object)]
    
    