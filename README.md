# Incident Management System

REST API сервис для управления инцидентами, построенный на FastAPI, SQLAlchemy и PostgreSQL.

## Основные возможности

- **CRUD операции** для инцидентов
- **Пагинация и фильтрация** инцидентов по статусу
- **Миграции базы данных** через Alembic
- **Полностью асинхронный** код
- **Валидация данных** через Pydantic
- **Docker контейнеризация**

## Технологии

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: PostgreSQL
- **Async**: asyncpg, asyncio
- **Migrations**: Alembic
- **Container**: Docker, Docker Compose
- **Logging**: Python logging с JSON форматом

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/djsega1/ucar-test-task
cd ucar-test-task
```

### 2. Настройка окружения
Копируем файл с переменными окружения
```
make env
make env-win # (для Windows)
```

### 3. Запуск через Docker

> make setup

### 4. Краткое описание эндпоинтов

Есть 3 эндпоинта:
1. `GET /api/v1/incidents/`  
    Принимает на вход номер страницы, размер страницы и Enum-фильтр для статуса инцидента, возвращает список значений и кол-во страниц. К примеру:
    ```json
    {
        "values": [
            {
            "created_at": "2025-11-09T00:06:51.876750",
            "updated_at": "2025-11-09T00:06:51.876750",
            "description": "string",
            "source": "operator",
            "status": "new",
            "id": 1
            }
        ],
        "total_pages": 1
    }
    ```
2. `POST /api/v1/incidents/`  
    Принимает на вход строковое описание, Enum статуса и Enum источника инцидента, возвращает созданный инцидент. К примеру:
    ```json
    {
        "created_at": "2025-11-09T00:43:21.653Z",
        "updated_at": "2025-11-09T00:43:21.653Z",
        "description": "string",
        "source": "operator",
        "status": "new",
        "id": 0
    }
    ```
3. `PUT /api/v1/incidents/{incident_id}`  
    Принимает и возвращает то же, что и POST ручка, но параметры передать можно выборочно.

### 5. Сущности статуса и источника инцидента
<img width="416" height="391" alt="image" src="https://github.com/user-attachments/assets/89f1d449-8e0f-4fab-92aa-ab43bbaf108f" />

## Доп. пояснения
Приложение после запсука доступно по адресу `http://127.0.0.1/docs`  
В этом проекте из-за его компактности нет тестов и какой-то крутой логики с асинхронностью и микросервисами, он используется для демонстрации стиля написания моего кода.
