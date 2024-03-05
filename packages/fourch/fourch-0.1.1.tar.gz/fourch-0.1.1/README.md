# FourCH Python Library

FourCH - это асинхронная библиотека Python для взаимодействия с API сайта 4chan. Она предоставляет простой интерфейс для получения постов и вложений из различных разделов.

## Установка

Вы можете установить библиотеку с помощью pip:

```bash
pip install fourch
```

## Использование

```python
import asyncio
from fourch.api import FourCH
from fourch.const import Board

async def main():
    fch = FourCH(board=Board.S)
    
    # Получить посты из первой страницы
    result = await fch.get_post(1)
    print(result.threads[0].posts[0].filename)
    
    # Получить все вложения из указанного треда
    attachments = await fch.get_all_attachments(thread_number)
    print(attachments)
    
    # Получить вложения из всех тредов на первой странице
    thread_attachments = await fch.get_attachments_in_thread(page=1)
    print(thread_attachments)

asyncio.run(main())
```

## Методы

### `get_post(page: int) -> Model`

Получить посты из указанной страницы раздела.

### `get_all_attachments(thread_number: int) -> dict`

Получить все вложения из указанного треда в виде словаря, где ключ - имя треда, значение - список вложений.

### `get_attachments_in_thread(page: int) -> list`

Получить вложения из всех тредов на указанной странице раздела в виде списка.
