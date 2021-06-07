## Установка

Копировать репозиторий
```
clone https://github.com/nurlybek-dev/polls-test.git
cd polls-test
```

Установить зависимости используя виртуальное окружение либо систему.
Для pipenv

```
pipenv install
pipenv shell
```
Для virtualenv
```
virtualenv venv
source venv\Scripts\activate
# Для Windows
venv\Scripts\activate
```

С активированным виртуальным окружением создаём базу данных
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Создаём суперпользователя
```sh
python manage.py createsuperuser
```

## API

Endpoints:
- /admin/ - Django Admin Panel
- /api-auth/login/ - DRF Login
- /api-auth/logout/ - DRF Logout
- /api/ - ApiRoot
- /api/admin/polls/ - ViewSet опросников, доступ только для админов
- /api/admin/questions/ - ViewSet вопросов, доступ только для админов
- /api/admin/options/ - ViewSet вариантов ответов, доступ только для админов
- /api/admin/answers/ - ViewSet ответов пользователей, доступ только для админов
- /api/polls/ - Список доступных опросников на данный момент
- /api/polls/{pk} - Детальный просмотр опросника с вложенными вопросами
- /api/answers/{pk} - Список все пройденных опросников с ответами


# Admin
## Polls - admin
Для создания опроса необходимо передать следующие данные
```
{
    "name": String,
    "start_date": String,
    "end_date": String,
    "description": Text
}
```

## Questions - admin
Для создания вопросов необходимо передать следующие данные. Можно передать варианты ответов в списке _options_ либо отдельно через его api.
```
{
    "poll": poll id,
    "text": String,
    "type": Integer,
    "options": [ Optional
        {"text": String}
    ]
}
```

## Options - admin
Для создания варантов ответов для вопроса необходимо передать следующие данные
```
{
    "question": question id,
    "text": String
}
```

## Answers - admin
Для создания ответов необходимо передать следующие данные
```
{
    "question": question id,
    "choice": choice id,
    "text": String
}
```


# User

## Polls - user
Пользователь получает список доступных опросов через _/api/polls/_. 

Ответ присыает туда же POST запросом. Данные которые нужно отправить.

Одно из двух _text_ или _choice_. Программа допускает заполнения обоих полей.
```
{
    "user_id": user id,
    "poll_id": poll id,
    "answers": [
        {
            "question": id, 
            "text": String,
            "choice": Integer
        }
    ]
}
```

## Answers - user
Для получения ответов пользователя _/api/answers/{pk}/_
Вернет список все пройденных опросников.
