# Платформа онлайн-навчання (Online Learning Platform)

Монолітний вебзастосунок для організації онлайн-навчання: створення курсів, уроків, запису студентів, відстеження їхнього прогресу та проходження тестів.

## Архітектура та структура проєкту
Проєкт реалізовано за багатошаровою архітектурою з чітким розподілом відповідальностей:
* Controller / API Layer (views.py) — обробка HTTP-запитів та повернення відповідей.
* Service Layer (services.py) — реалізація бізнес-логіки застосунку.
* Repository & Data Layer (repositories.py, models.py) — абстракція доступу до даних та ORM-моделі Django.

### Доменна модель даних (Етап 1):
* User — користувачі системи з ролями (Admin, Teacher, Student).
* Course — навчальні курси, створені викладачами.
* Lesson — уроки, що належать до конкретних курсів.
* Enrollment — записи студентів на курси.
* Progress — відстеження виконання уроків студентами.
* Quiz — тести до уроків у форматі JSON.

## Технології
* Мова програмування: Python 3.11+
* Фреймворк: Django 5.x
* API: Django REST Framework (DRF)
* База даних: SQLite / PostgreSQL

## Інструкція з локального запуску «з нуля»

Клонуйте репозиторій та перейдіть до папки проєкту:
git clone <url_вашого_репозиторію>
cd online_learning_platform

Створіть та активуйте віртуальне середовище Python для PowerShell:
python -m venv venv
.\venv\Scripts\Activate

Створіть та активуйте віртуальне середовище Python для CMD:
python -m venv venv
venv\Scripts\activate.bat

Створіть та активуйте віртуальне середовище Python для macOS або Linux:
python -m venv venv
source venv/bin/activate

Встановіть необхідні залежності:
pip install -r requirements.txt

Створіть та застосуйте міграції бази даних:
python manage.py makemigrations
python manage.py migrate

Створіть обліковий запис адміністратора:
python manage.py createsuperuser

Запустіть сервер розробки:
python manage.py runserver

## Перевірка працездатності

Адреса сервісу: http://127.0.0.1:8000/
Health Check endpoint: http://127.0.0.1:8000/health
Панель адміністратора: http://127.0.0.1:8000/admin/

Перевірка через термінал за допомогою курла:
curl http://127.0.0.1:8000/health

Очікувана відповідь сервера:
{"status": "ok", "database": "healthy"}