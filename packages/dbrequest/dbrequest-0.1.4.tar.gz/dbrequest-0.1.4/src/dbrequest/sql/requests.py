from typing import Tuple, Union, Any

from .interfaces import ISQLRequest
from .properties import TableProp, ColumnsProp, ValuesProp, WhereProp, OrderByProp, LimitProp


class SQLInsert(ISQLRequest, TableProp, ColumnsProp, ValuesProp):
    def __init__(self) -> None:
        TableProp.__init__(self)
        ColumnsProp.__init__(self, allow_all=False)
        ValuesProp.__init__(self)
        self._is_default = False
        self._is_replace = False

    def setDefaultValues(self) -> None:
        self._is_default = True

    def setReplaceMode(self) -> None:
        self._is_replace = True

    def setArgs(
            self,
            table: str = None,
            columns: Tuple[str] = None,
            values: Tuple[Any] = None,
            is_default: bool = None,
            is_replace: bool = None
        ) -> None:

        if table is not None: self.table = table
        if self._table is None: raise ValueError(table)
        if columns is not None: self.columns = columns
        if self._columns is None: raise ValueError(columns)
        if values is not None: self.values = values
        if self._values is None: raise ValueError(values)
        if isinstance(is_default, bool): self._is_default = is_default
        if isinstance(is_replace, bool): self._is_replace = is_replace

    def getRequest(self) -> Tuple[str, Tuple[Any]]:
        request: Tuple[str, str] = ()

        command = 'INSERT'
        if self._is_replace:
            command = 'REPLACE'
        
        request_str = f'{command} INTO {self._table} ({self._columnsStr}) '

        if self._is_default:
            request_str += 'DEFAULT VALUES;'
            request = (request_str, )
        else:
            request_str += f'VALUES ({self._valuesTemplate});'

            request = (request_str, self._values)

        return request
    
class SQLSelect(ISQLRequest, TableProp, ColumnsProp, WhereProp, OrderByProp, LimitProp):
    def __init__(self) -> None:
        TableProp.__init__(self)
        ColumnsProp.__init__(self, allow_all=True)
        WhereProp.__init__(self)
        OrderByProp.__init__(self)
        LimitProp.__init__(self)
        self._is_distinct: bool = False 

    def setDistinct(self) -> None:
        self._is_distinct = True

    def setArgs(
            self,
            table: str = None,
            columns: Union[Tuple[str], str] = None,
            where: str = None,
            is_distinct: bool = None,
            order_by: str = None,
            limit: Union[int, str] = None
        ) -> None:

        if table is not None: self.table = table
        if self._table is None: raise ValueError(table)
        if columns is not None: self.columns = columns
        if self._columns is None: raise ValueError(columns)
        if where is not None: self.where = where
        if isinstance(is_distinct, bool): self._is_distinct = is_distinct
        if order_by is not None: self.orderBy = order_by
        if limit is not None: self.limit = limit
        
        
    def getRequest(self) -> Tuple[str]:
        distinct = ''
        if self._is_distinct:
            distinct = ' DISTINCT'

        request_str = f'SELECT{distinct} {self._columnsStr} FROM {self._table}{self._whereStr}{self._orderStr}{self._limitStr};'

        return (request_str, )

class SQLUpdate(ISQLRequest, TableProp, ColumnsProp, ValuesProp, WhereProp):
    def __init__(self) -> None:
        TableProp.__init__(self)
        ColumnsProp.__init__(self, allow_all=False)
        ValuesProp.__init__(self)
        WhereProp.__init__(self)

    def setArgs(self, table:str=None, columns:Tuple[str]=None, values:tuple=None, where:str=None) -> None:
        if table is not None: self.table = table
        if self._table is None: raise ValueError(table)
        if columns is not None: self.columns = columns
        if self._columns is None: raise ValueError(columns)
        if values is not None: self.values = values
        if self._values is None: raise ValueError(values)
        if where is not None: self.where = where

    def getRequest(self) -> Tuple[str, Tuple[Any]]:
        request: Tuple[str, str] = ()

        columns_and_values = ', '.join([f'{column} = ?' for column in self._columns])
        request_str = f'UPDATE {self._table} SET {columns_and_values}{self._whereStr};'

        request = (request_str, self._values)

        return request

class SQLDelete(ISQLRequest, TableProp, WhereProp):
    def __init__(self) -> None:
        TableProp.__init__(self)
        WhereProp.__init__(self)

    def setArgs(self, table:str=None, where:str=None) -> None:
        if table is not None: self.table = table
        if self._table is None: raise ValueError(table)
        if where is not None: self.where = where

    def getRequest(self) -> Tuple[str]:
        request_str = f'DELETE FROM {self._table}{self._whereStr};'

        return (request_str, )

class SQLCustom(ISQLRequest):
    def __init__(self) -> None:
        self._request_str:str = None

    def setArgs(self, request:str) -> None:
        if not isinstance(request, str):
            raise TypeError(request)
        if request == '':
            raise ValueError(request)
        self._request_str = request

    def getRequest(self) -> Tuple[str]:
        return (self._request_str, )

class SQLFile(ISQLRequest):
    def __init__(self) -> None:
        self._request_str = None

    def setArgs(self, filename:str) -> None:
        with open(filename, 'r') as file:
            self._request_str = file.read()
                
    def getRequest(self) -> Tuple[str]:
        return (self._request_str, )

