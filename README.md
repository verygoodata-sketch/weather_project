# weather_project
# Погода в Пушкино
КТ Породнова Алексея по Python on Web 
Веб-приложение на **Django** для отображения погодных данных в городе **Пушкино**.  
Проект содержит:
- страницу с прогнозом погоды на ближайший час, день и неделю;
- регистрацию и авторизацию пользователей;
- проверку существующих пользователей;
- одну базу данных SQLite;

---

## Возможности

- Регистрация нового пользователя
- Вход и выход из аккаунта
- Отображение прогноза погоды:
  - на ближайший час
  - на день
  - на неделю
- Проверка на существующего пользователя при регистрации

---

## Технологии

- Python
- Django
- HTML
- CSS
- SQLite
- Requests

---

## Структура проекта
weather_project/
├── manage.py
├── db.sqlite3
├── weather_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── __pycache__/
│       ├── __init__.cpython-313
│       ├── settings.cpython-313
│       ├── urls.cpython-313
│       └── wsgi.cpython-313
└── weather_app/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    ├── __pycache__/
    │   ├── __init__.cpython-313
    │   ├── admin.cpython-313
    │   ├── apps.cpython-313
    │   ├── forms.cpython-313
    │   ├── models.cpython-313
    │   ├── urls.cpython-313
    │   └── views.cpython-313
    ├── templates/
    │   ├── base.html
    │   ├── weather/
    │   │   └── home.html
    │   └── auth/
    │       ├── login.html
    │       └── register.html
    └── static/
        └── css/
            └── style.css

---

## Установка и запуск

### 1. Клонировать репозиторий (git clone <ссылканарепозиторий>; cd weather_project)
### 2. Установить зависимости (pip install django requests)
### 3. Создать миграции (python manage.py makemigrations; python manage.py migrate)
### 4. Создать суперпользователя (python manage.py createsuperuser)
### 5. Запустить сервер (python manage.py runserver)
### 6. Открыть сайт 

---

---

## Авторизация
Для доступа к главной странице нужно войти в аккаунт.
Уже есть один готовый аккаунт.
{Имя пользователя - Джон Доу;
Пароль - FghruYuRt;}

---

## Примечание
Если погодный API временно недоступен, сайт показывает запасные данные.
