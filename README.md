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

## Архітектура бази даних (ER-діаграма)

Нижче наведено повну ER-діаграму бази даних платформи, яка охоплює всі 4 етапи розробки:

```mermaid
erDiagram
    User ||--o{ Course : "creates / teaches (Stage 1)"
    User ||--o{ Enrollment : "enrolls (Stage 1)"
    Course ||--o{ Enrollment : "has (Stage 1)"
    Course ||--o{ Lesson : "contains (Stage 1)"
    Lesson ||--o{ Quiz : "has (Stage 2)"
    Quiz ||--|{ Question : "contains (Stage 2)"
    User ||--o{ BackgroundJob : "triggers (Stage 4)"

    User {
        int id PK
        string username
        string email
        string password
    }

    Course {
        int id PK
        string title
        text description
        string cover_image "Stage 3: File storage"
        datetime created_at "Stage 4: Composite Index"
        int teacher_id FK
    }

    Enrollment {
        int id PK
        datetime enrolled_at
        int user_id FK
        int course_id FK
    }

    Lesson {
        int id PK
        string title
        text content
        int course_id FK
    }

    Quiz {
        int id PK
        string title
        int lesson_id FK
    }

    Question {
        int id PK
        text text
        json options
        int correct_option
        int quiz_id FK
    }

    BackgroundJob {
        uuid job_id PK "Stage 4: In-memory JOBS_DB"
        string status "pending | processing | done"
        json payload
    }
