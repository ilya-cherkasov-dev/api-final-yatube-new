# api_final_yatube

REST API для социальной сети **Yatube**: публикации, группы, комментарии
и подписки на авторов.

## Описание проекта

Через API можно:

- читать публикации, группы и комментарии без регистрации;
- публиковать посты (в том числе в группе и с картинкой), редактировать
  и удалять **только свои**;
- комментировать посты и управлять своими комментариями;
- подписываться на авторов и искать среди своих подписок.

Аутентификация — по **JWT-токену**. Анонимным пользователям API доступен
только на чтение, кроме подписок: работа с ними требует токена.
При попытке изменить чужой пост или комментарий API возвращает
`403 Forbidden`.

Полная документация доступна после запуска проекта по адресу
[http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/).

## Технологии

- Python 3.14
- Django 5.2
- Django REST Framework 3.17
- Djoser + Simple JWT

## Установка

1. Клонировать репозиторий и перейти в него:

   ```bash
   git clone https://github.com/ilya-cherkasov-dev/api-final-yatube-new.git
   cd api-final-yatube-new
   ```

2. Создать и активировать виртуальное окружение:

   ```bash
   python -m venv venv
   # Windows
   source venv/Scripts/activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. Установить зависимости:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Выполнить миграции:

   ```bash
   cd yatube_api
   python manage.py migrate
   ```

5. Запустить проект:

   ```bash
   python manage.py runserver
   ```

## Примеры запросов

### Получить JWT-токен

```http
POST /api/v1/jwt/create/
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}
```

Ответ:

```json
{
    "refresh": "string",
    "access": "string"
}
```

Токен передаётся в заголовке каждого запроса:

```
Authorization: Bearer <access-токен>
```

### Создать публикацию

```http
POST /api/v1/posts/
Content-Type: application/json
Authorization: Bearer <access-токен>

{
    "text": "Текст публикации",
    "group": 1
}
```

Ответ:

```json
{
    "id": 1,
    "author": "username",
    "text": "Текст публикации",
    "pub_date": "2026-11-21T10:00:00Z",
    "image": null,
    "group": 1
}
```

### Получить публикации с пагинацией

```http
GET /api/v1/posts/?limit=10&offset=0
```

Без параметров `limit` и `offset` возвращается полный список.

### Добавить комментарий

```http
POST /api/v1/posts/1/comments/
Content-Type: application/json
Authorization: Bearer <access-токен>

{
    "text": "Текст комментария"
}
```

### Подписаться на автора

```http
POST /api/v1/follow/
Content-Type: application/json
Authorization: Bearer <access-токен>

{
    "following": "username"
}
```

### Найти автора среди своих подписок

```http
GET /api/v1/follow/?search=username
Authorization: Bearer <access-токен>
```

## Автор

Ilya Cherkasov
