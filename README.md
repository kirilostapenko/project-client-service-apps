# Платформа онлайн-навчання (Online Learning Platform)

Монолітний вебзастосунок для організації онлайн-навчання: створення курсів, уроків, запису студентів, відстеження їхнього прогресу та проходження тестів.

## Архітектура та структура проєкту
Проєкт реалізовано за суворою багатошаровою архітектурою з чітким розподілом відповідальностей:
- Controller / API Layer (views.py) — обробка HTTP-запитів, валідація через серіалізатори та повернення відповідей.
- Service Layer (services.py) — реалізація бізнес-логіки застосунку та перевірка вхідних даних.
- Repository & Data Layer (repositories.py, models.py) — абстракція доступу до даних та ORM-моделі Django.

### Доменна модель даних та ієрархія (Етап 2):
- User — користувачі системи з ролями (Admin, Teacher, Student).
- Course — навчальні курси, створені викладачами (з підтримкою вкладеного створення через ендпоінти).
- Lesson — уроки, що належать до конкретних курсів (`/api/courses/<course_id>/lessons/`).
- Quiz — тести до уроків (`/api/lessons/<lesson_id>/quizzes/`).
- Enrollment — записи студентів на курси.
- Progress — відстеження виконання уроків студентами.

## Технології
- Мова програмування: Python 3.11+
- Фреймворк: Django 5.x
- API: Django REST Framework (DRF)
- База даних: SQLite / PostgreSQL

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

## Перевірка працездатності та API

Адреса сервісу: http://127.0.0.1:8000/
Health Check endpoint: http://127.0.0.1:8000/health
Панель адміністратора: http://127.0.0.1:8000/admin/

### Основні API ендпоінти (Етап 2):
- Список та створення курсів: `POST /api/courses/`
- Деталі курсу: `GET /api/courses/<id>/`
- Створення уроку для курсу: `POST /api/courses/<course_id>/lessons/`
- Створення тесту для уроку: `POST /api/lessons/<lesson_id>/quizzes/`

Перевірка через термінал за допомогою курла:
curl http://127.0.0.1:8000/health

Очікувана відповідь сервера:
{"status": "ok", "database": "healthy"}

## Етап 3: Документування, тестування та робота з файлами
- **Документація API**: інтегровано `drf-spectacular`. Доступна інтерактивна документація Swagger UI за адресою `http://127.0.0.1:8000/api/docs/`.
- **Робота з файлами**: реалізовано безпечне завантаження обкладинок курсів (`POST /api/courses/{id}/cover/`) із перевіркою розміру (до 5 МБ) та форматів (JPEG, PNG), а також їх отримання (`GET /api/courses/{id}/cover/`).
- **Тестування**: додано інтеграційні тести для перевірки бізнес-логіки та файлових операцій (`python manage.py test`).