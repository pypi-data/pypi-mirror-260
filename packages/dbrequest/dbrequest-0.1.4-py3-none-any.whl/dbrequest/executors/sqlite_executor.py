import sqlite3
import logging
from typing import List, Tuple, Any

from ..config import config
from ..sql_requests import SQLFile
from .interfaces import ISQLRequest, IDatabaseExecutor


class SQLiteExecutor(IDatabaseExecutor):
    def __init__(self, database_filename:str=None) -> None:
        self._logger = logging.getLogger(config.LOGGER_NAME)
        self._database_filename = database_filename
    
    def start(self, sqlRequest:ISQLRequest) -> List[Tuple[Any]]:
        if not isinstance(sqlRequest, ISQLRequest):
            raise TypeError(type(sqlRequest))
        
        database_filename = config.DATABASE_FILENAME if self._database_filename is None else self._database_filename
        connection = None

        try:
            connection = sqlite3.connect(database_filename)
            cursor = connection.cursor()

            request = sqlRequest.getRequest()
            request_log = '\n'.join(str(line) for line in request)
            self._logger.debug(f'Running request:\n{request_log}')
            
            if isinstance(sqlRequest, SQLFile):
                cursor.executescript(request[0])
            else:
                cursor.execute(*request)
            
            response = None
            if request[0].split()[0].upper() == 'SELECT':
                response = cursor.fetchall()
            
            connection.commit()

            cursor.close()

        except sqlite3.Error as error:
            self._logger.exception(error)
            raise

        finally:
            if connection is not None:
                self._logger.debug(f'Lines changed: {connection.total_changes}')
                connection.close()
        
        return response
        
