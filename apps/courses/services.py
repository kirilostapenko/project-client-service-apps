from typing import List, Optional
from apps.courses.models import Course, Lesson
from apps.courses.repositories import CourseRepository, LessonRepository
from .models import Quiz, Lesson
from .repositories import QuizRepository
import os
import requests
from django.core.cache import cache

class CourseService:
    def __init__(self):
        self.course_repo = CourseRepository()
        self.lesson_repo = LessonRepository()

    def get_all_courses(self) -> List[Course]:
        return self.course_repo.get_all()

    def get_course_details(self, course_id: int) -> Optional[Course]:
        return self.course_repo.get_by_id(course_id)

    def create_course(self, title: str, description: str, teacher) -> Course:
        if not title:
            raise ValueError("Назва курсу обов'язкова")
        if not teacher:
            raise ValueError("Курс повинен мати викладача")
        return self.course_repo.create(title=title, description=description, teacher=teacher)

    def update_course(self, course_id: int, **data) -> Optional[Course]:
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return None
        return self.course_repo.update(course, **data)

    def delete_course(self, course_id: int) -> bool:
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return False
        self.course_repo.delete(course)
        return True

    def add_lesson_to_course(self, course_id: int, title: str, content: str, order: int) -> Lesson:
        course = self.course_repo.get_by_id(course_id)
        if not course:
            raise ValueError("Курс не знайдено")
        if not title:
            raise ValueError("Назва уроку обов'язкова")
        
        return self.lesson_repo.create(
            course=course,
            title=title,
            content=content,
            order=order
        )

    def upload_course_cover(self, course_id: int, image_file) -> Course:
        course = self.course_repo.get_by_id(course_id)
        if not course:
            raise ValueError("Курс не знайдено.")

        if not image_file:
            raise ValueError("Файл не передано.")
    
        max_size_bytes = 5 * 1024 * 1024
        if image_file.size > max_size_bytes:
            raise ValueError("Розмір файлу перевищує 5 МБ.")
        
        allowed_types = ['image/jpeg', 'image/png']
        content_type = getattr(image_file, 'content_type', '')
        if content_type and content_type not in allowed_types:
            raise ValueError("Дозволені лише формати JPEG або PNG.")

        if course.cover_image:
            course.cover_image.delete(save=False)

        course.cover_image = image_file
        course.save()
        return course
    
    def get_course_cover(self, course_id: int):
        course = self.course_repo.get_by_id(course_id)
        if not course:
            raise ValueError("Курс не знайдено.")
        if not course.cover_image:
            raise ValueError("У курсу немає обкладинки.")
        return course.cover_image

class LessonService:
    def __init__(self):
        self.lesson_repo = LessonRepository()
        self.course_repo = CourseRepository()

    def get_course_lessons(self, course_id: int):
        return self.lesson_repo.get_by_course(course_id)

    def create_lesson(self, course_id: int, title: str, content: str, order: int) -> Lesson:
        course = Course.objects.filter(id=course_id).first()
        if not course:
            raise ValueError("Курс не знайдено")
        if not title:
            raise ValueError("Назва уроку обов'язкова")
        
        return self.lesson_repo.create(
            course=course,
            title=title,
            content=content,
            order=order
        )

class QuizService:
    def __init__(self):
        self.quiz_repo = QuizRepository()

    def create_quiz(self, lesson_id: int, title: str) -> Quiz:
        lesson = Lesson.objects.filter(id=lesson_id).first()
        if not lesson:
            raise ValueError("Урок не знайдено")
        if not title:
            raise ValueError("Назва тесту обов'язкова")
        return self.quiz_repo.create(lesson=lesson, title=title)

class ExternalGeocodingService:
    BASE_URL = "https://api.geoapify.com/v1/geocode/search"

    @classmethod
    def geocode(cls, address: str):
        if not address:
            return None
            
        cache_key = f"geo_{address.strip().lower()}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        api_key = os.getenv("GEOCODING_API_KEY", "")
        if not api_key:
            return None

        try:
            response = requests.get(
                cls.BASE_URL,
                params={"text": address, "apiKey": api_key, "format": "json"},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if results:
                    coords = {"lat": results[0]["lat"], "lon": results[0]["lon"]}
                    cache.set(cache_key, coords, timeout=3600)
                    return coords
                else:
                    cache.set(cache_key, {}, timeout=600)
                    return None
            else:
                return None
        except (requests.RequestException, Exception):
            return None