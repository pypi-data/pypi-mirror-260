from enum import Enum
from typing import Union

from ..executors.interfaces import IDatabaseExecutor


class Executors(Enum):
    SQLITE = 'SQLite'

DATABASE_FILENAME: str = 'database.db'
EXECUTOR: Union[Executors, IDatabaseExecutor] = Executors.SQLITE
LOGGER_NAME: str = 'database'

def init(
        database_filename: str = 'database.db',
        executor: Union[str, Executors, IDatabaseExecutor] = Executors.SQLITE,
        logger_name: str = 'database',
        init_script: str = None,
    ) -> None:

    global DATABASE_FILENAME
    global EXECUTOR
    global LOGGER_NAME

    if not isinstance(database_filename, str): raise TypeError(type(database_filename))
    if not isinstance(executor, (str, Executors, IDatabaseExecutor)): raise TypeError(executor)
    if not isinstance(logger_name, str): raise TypeError(type(logger_name))
    if not isinstance(init_script, (str, type(None))): raise TypeError(type(init_script))

    if database_filename == '': raise ValueError(database_filename)
    if logger_name == '': raise ValueError(logger_name)
    if init_script is not None and init_script == '': raise ValueError(init_script)

    if isinstance(executor, str):
        executor = Executors(executor)
    EXECUTOR = executor
    
    DATABASE_FILENAME = database_filename
    LOGGER_NAME = logger_name

    if init_script is not None:
        from ..executors.universal_executor import UniversalExecutor
        from ..sql_requests import SQLFile

        request = SQLFile()
        request.setArgs(filename=init_script)

        executor = UniversalExecutor()
        executor.start(request)

