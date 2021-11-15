# API_YAMDB

---

### Описание

---
Проект предназначен для создания пользователями отзывов, содержаших текст и оценку, на произведения. Произведения имеют различные жанры и категорию, жанров может быть несколько.
Пользователь может оставить только один отзыв одному произведению. Отзывы могут быть прокомментированы.

### Категории пользователей

---
Пользователи делятся на 5 категорий:
1) Суперюзер - SuperUser
2) Админ - Admin
3) Модератор - Moderator
4) Авторизованный пользователь - User (присваивается всем новым пользователям)
5) Неавторизованный пользователь - UnauthUser
---

### Права пользователей

---
UnauthUser:
Просмотр описания произведений, чтение отзывов и комментариев
---

---
User:
Просмотр описания произведений, чтение отзывов и комментариев
Публикация отзывов, комментариев
Редактирование/удаление своих отзывов/комментариев
---

---
Moderator:
Просмотр описания произведений, чтение отзывов и комментариев
Публикация отзывов, комментариев
Редактирование/удаление ВСЕХ отзывов/комментариев
---

---
SuperUser / Admin:
Полные права на все действия
---

### Технологии

---

Для API в проекте созданы сериализаторы и вью сеты для каждой модели:

Model           Serializer          ModelViewSet
---
Title    -  TitleBaseSerializer  -  TitleViewSet
            TitlePostSerializer 
Genre    -  GenreSerializer      -  GenreViewSet
Category -  CategorySerializer   -  CategoryViewSet
Review   -  ReviewSerializer     -  ReviewViewSet
Comment  -  CommentSerializer    -  CommentViewSet

---

### Установка

---

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/camousmen/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

---

### Примеры работы API
---

GET-запрос на /api/v1/titles/

    Форма:
QUERY PARAMS
category - string (фильтрует по полю slug категории)
genre - string (фильтрует по полю slug жанра)
name - string (фильтрует по названию произведения)
year - integer (фильтрует по году)

    Ответ:
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": []
  }
]

---

GET-запрос на /api/v1/titles/{title_id}

    Форма:
PATH PARAMETERS
title_id(required) - integer(ID объекта)

    Ответ:
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
 "genre": [
    {}
  ],
  "category": {
  "name": "string",
  "slug": "string"
  }
}

---

GET-запрос на /api/v1/titles/{title_id}/reviews

   Форма:
PATH PARAMETERS
title_id(required) - integer(ID объекта)

    Ответ:
[
  {
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": []
}
]

---

PATCH-запрос на /api/v1/users/{username}
   Форма:
PATH PARAMETERS
username(required) - string(Username пользователя)

REQUEST BODY SCHEMA
username(required) - string <= 150 characters ^[\w.@+-]+\z
email(required) - string <email> <= 254 characters
first_name - string(<= 150 characters)
last_name - string (<= 150 characters)
bio - string
role - string(Enum: "user" "moderator" "admin")

---

С полным списком можно ознакомиться по ссылке http://127.0.0.1:8000/redoc/
