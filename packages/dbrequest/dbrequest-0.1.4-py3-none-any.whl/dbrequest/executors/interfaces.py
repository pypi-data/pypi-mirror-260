from typing import List, Tuple, Any

from ..sql.interfaces import ISQLRequest

class IDatabaseExecutor:
    def __init__(self, database_filename:str=None) -> None:
        raise NotImplementedError()

    def start(self, sqlRequest:ISQLRequest) -> List[Tuple[Any]]:
        raise NotImplementedError()
    
