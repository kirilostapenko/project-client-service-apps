# Платформа онлайн-навчання (Online Learning Platform)

Монолітний вебзастосунок для організації онлайн-навчання: створення курсів, уроків, запису студентів, відстеження їхнього прогресу, проходження тестів та асинхронної обробки фонових задач.

## Архітектура та структура проєкту
Проєкт реалізовано за суворою багатошаровою архітектурою з чітким розподілом відповідальностей:
- Controller / API Layer (views.py) — обробка HTTP-запитів, валідація через серіалізатори та повернення відповідей.
- Service Layer (services.py) — реалізація бізнес-логіки застосунку та перевірка вхідних даних.
- Repository & Data Layer (repositories.py, models.py) — абстракція доступу до даних та ORM-моделі Django (з урахуванням оптимізації та індексів).
- Async / Background Jobs (jobs.py) — керування фоновими асинхронними задачами у пам'яті за допомогою потоків.

### Доменна модель даних та ієрархія (Етап 4):
- User — користувачі системи з ролями (Admin, Teacher, Student).
- Course — навчальні курси, створені викладачами (з оптимізованим складеним індексом `(created_at, id)` та аннотацією кількості студентів).
- Lesson — уроки, що належать до конкретних курсів (`/api/courses/<course_id>/lessons/`).
- Quiz — тести до уроків (`/api/lessons/<lesson_id>/quizzes/`).
- Enrollment — записи студентів на курси.
- Progress — відстеження виконання уроків студентами.

## Технології
- Мова програмування: Python 3.11+
- Фреймворк: Django 5.x
- API: Django REST Framework (DRF)
- Документація: drf-spectacular (Swagger UI)
- Фонові задачі: Threading & UUID (асинхронне виконання в пам'яті)
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
Документація Swagger UI: http://127.0.0.1:8000/api/docs/

### Основні API ендпоінти (Етап 4):
- Список та створення курсів (оптимізовано): `GET /api/courses/`, `POST /api/courses/`
- Деталі курсу та оновлення: `GET /api/courses/<id>/`, `PUT /api/courses/<id>/`, `DELETE /api/courses/<id>/`
- Управління обкладинками: `GET /api/courses/{id}/cover/`, `POST /api/courses/{id}/cover/`
- Створення уроку для курсу: `POST /api/courses/<course_id>/lessons/`
- Створення тесту для уроку: `POST /api/lessons/<lesson_id>/quizzes/`
- Запуск фонової задачі: `POST /api/jobs/start/`
- Перевірка статусу задачі: `GET /api/jobs/<job_id>/`

Перевірка через термінал за допомогою курла:
curl http://127.0.0.1:8000/health

Очікувана відповідь сервера:
{"status": "ok", "database": "healthy"}

## Попередні етапи та особливості розробки
- **Етап 3**: Інтегровано `drf-spectacular` (Swagger), реалізовано безпечне завантаження обкладинок курсів та додано інтеграційні тести.
- **Етап 4**: Вирішено проблеми дублювання моделей, додано складений індекс бази даних `(created_at, id)`, усунено помилки маршрутизації та реалізовано повноцінний асинхронний моніторинг фонових задач (`pending` -> `processing` -> `done`).