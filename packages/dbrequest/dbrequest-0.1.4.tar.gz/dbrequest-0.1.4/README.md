# dbrequest

dbrequest is a library for easy database handling. The library is primarily designed for simple projects where complex SQL queries are not needed and SQLite can be used as the DBMS (although the library supports other DBMS as well).

The library provides an abstraction from the DBMS and allows working with storing, loading, modifying, and deleting object-containers without explicit use of SQL.

[Read this in Russian](https://github.com/korandr/dbrequest/blob/main/README.ru.md) 

## Contents

- [Installation](#installation)
- [Disclaimer](#disclaimer)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Feedback](#feedback)

## Installation

Installation from the PyPI repository:

```bash
$ pip install dbrequest
```

Installation from a GitHub repository (requires pip version 20 and above).

```bash
$ pip install git+https://github.com/korandr/dbrequest.git
```

Library import:

```python
import dbrequest
```

## Disclaimer

The library is primarily developed for the developer's personal projects and does not prioritize suitability for any projects.

Some restrictions are used in the library (for example, all objects to be saved must have an id of type int), which are convenient for the developer's projects but may not necessarily be suitable for other projects.

Nevertheless, the developer is not against integrating this library into other projects if it solves the necessary tasks.

The library does not adhere to the PEP code style and is unlikely to do so. Objects, methods, and properties are always named using camelCase here. However, an important task is to adhere to the SOLID principles.

## Quick Start

For example, let's create a table `users`. Describe it in the file `create_table.sql`.

```sql
create table IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    last_message TEXT DEFAULT NULL
);
```

Let's initialize the library.

```python
import dbrequest

dbrequest.init(init_script='create_table.sql')
```

Next, in the file `user.py`, let's create a class `User`. Inheriting from `Savable` will automatically add the `_id` field and the `id` property to the class, which is the implementation of the `dbrequest.ISavable` interface.

```python
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
```

Now let's create the file `user_fields.py` and implement classes in it that will be used by the library to load and save fields of the `User` class in the database.

```python
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
```

If needed, these classes can contain additional logic for data processing when exchanging data between the container class and the database. For example, converting non-standard data types to data types supported by the database.

The last step is to create a class for database requests related to the user. Let's create the file `user_request.py`.

```python
from dbrequest import AbstractDBRequest
from dbrequest import IdField

from user_fields import *

class UserDBRequest(AbstractDBRequest):
    def __init__(self) -> None:
        super().__init__()
        self._TABLE_NAME = 'users'
        self._FIELDS = (
            IdField(),
            UserUsernameField('username', str),
            UserLastMessageField('last_message', str, allowed_none=True)
        )
```

In `self._TABLE_NAME`, specify the name of the corresponding table.

Through the property `self._FIELDS`, the connection with columns in the database is established. The method takes a tuple of implementations of `AbstractField`. The fields should be arranged in the same order as the columns in the database. In the constructor of each field class, specify the column name and its type. If the column can accept a `NULL` value, then `allowednone=True` must be defined.

The abstraction is created. Now it is convenient to perform operations with the `User` class and the database.

```python
from typing import Tuple

from user import User
from user_request import UserDBRequest


user = User()
user.username = 'simple_user'

request = UserDBRequest()
request.save(user)

user: User = request.loadAll(User(), limit=1)[0]
print(user.id)

sameUser = User()
sameUser.id = user.id
request.load(sameUser)
print(sameUser.username)

user.lastMessage = 'Hello world!'
request.update(user)

admin = User()
admin.username = 'admin'
admin.lastMessage = 'Do you want to be banned?'

request.save(admin)

users: Tuple[User] = request.loadAll(User())
for user in users:
    print(f'The user who said "{user.lastMessage}" has been deleted')
    request.delete(user)
```

[See the code from the example](https://github.com/korandr/dbrequest/tree/main/example)

## Documentation

The documentation for the library is only [available in Russian](https://github.com/korandr/dbrequest/wiki). If you are genuinely interested in the documentation, I suggest using Google Translate as a browser extension, as it works really well.

## Feedback

Developer: Andrey Korovyanskiy | [korandrmail@ya.ru](mailto:korandrmail@ya.ru)
