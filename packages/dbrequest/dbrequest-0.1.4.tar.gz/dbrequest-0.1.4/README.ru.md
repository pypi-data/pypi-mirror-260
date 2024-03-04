# dbrequest
dbrequest это библиотека для удобной работы с базами данных. Библиотека предназначена в первую очередь для простых проектов, в которых не нужны сложные SQL-запросы и в качестве СУБД может быть использована SQLite (хотя библиотека позволяет работать с другими СУБД). 

Библиотека предоставляет абстракцию от СУБД и позволяет работать с сохранением, загрузкой, изменением и удалением объектов-контейнеров без явного использования SQL.

## Содержание
- [Установка](#установка)
- [Дисклеймер](#дисклеймер)
- [Быстрый старт](#быстрый-старт)
- [Документация](#документация)
- [Обратная связь](#обратная-связь)

## Установка

Из репозитория PyPI:

```bash
$ pip install dbrequest
```

Установка из github-репозитория (необходим pip версии 20 и выше)

```sh
$ pip install git+https://github.com/korandr/dbrequest.git
```

Импорт

```python
import dbrequest
```

## Дисклеймер

Библиотека разрабатывается в первую очередь для личных проектов разработчика и не ставит приоритетной целью пригодность для любых проектов.

В библиотеке используются некоторые ограничения (например, все сохраняемые объекты должны иметь id типа int), которые удобны для проектов разработчика, но не обязательно подойдут другим проектам. 

Тем не менее, разработчик не против внедрения этой библиотеки в другие проекты, если она решает необходимые задачи.

В библиотеке не соблюдён код-стайл PEP и вряд ли будет. Объекты, методы и свойства здесь всегда называются с помощью camelCase. Но при этом важной задачей является соблюдение принципов SOLID.

## Быстрый старт
Для примера создадим таблицу `users`. Опишем её в файле `create_table.sql`

```sql
create table IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    last_message TEXT DEFAULT NULL
);
```

Инициализируем библиотеку

```python
import dbrequest

dbrequest.init(init_script='create_table.sql')
```
Далее в файле `user.py` создадим класс `User`. Наследование от `Savable` автоматически добавит в класс поле `_id` и свойство `id`, что является реализацией интерфейса `dbrequest.ISavable`. 

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
Теперь создадим файл `user_fields.py` и реализуем в нём классы, с помощью которых библиотека будет загружать и сохранять поля класса `User` в базу данных. 

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
При необходимости эти классы могут содержать дополнительную логику обработки данных при обмене между классом-контейнером и базой данных. Например, приведение нестандартных типов данных к типам данных, поддерживаемых базой данных.  

Остаётся создать класс запросов в базу данных, связанных с пользователем. Создадим файл `user_request.py`

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
В `self._TABLE_NAME` указываем название соответствующей таблицы. 

С помощью свойства `self._FIELDS` задаётся связь со столбцами в базе данных. Метод принимает кортеж из реализаций `AbstractField`. Поля должны быть расположены в том же порядке, что и столбцы в базе данных. В конструкторе каждого класса поля указывается название столбца и его тип. Если столбец может принимать значение NULL, то необходимо определить `allowed_none=True`. 

Абстракция создана. Теперь можно удобно выполнять операции с классом `User` и базой данных

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

[Готовый код из этого примера](https://github.com/korandr/dbrequest/tree/main/example)

## Документация

[Здесь](https://github.com/korandr/dbrequest/wiki) можно ознакомиться с документацией к бибиотеке (только на русском)

## Обратная связь
Разработчик: Андрей Коровянский | [korandrmail@ya.ru](mailto:korandrmail@ya.ru) 
