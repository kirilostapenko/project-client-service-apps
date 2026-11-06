from typing import List, Optional
from apps.courses.models import Course, Lesson
from .models import Course, Lesson, Quiz

class CourseRepository:
    @staticmethod
    def get_all() -> List[Course]:
        return Course.objects.all()

    @staticmethod
    def get_by_id(course_id: int) -> Optional[Course]:
        return Course.objects.filter(id=course_id).first()

    @staticmethod
    def create(title: str, description: str, teacher) -> Course:
        return Course.objects.create(title=title, description=description, teacher=teacher)

    @staticmethod
    def update(course: Course, **data) -> Course:
        for key, value in data.items():
            setattr(course, key, value)
        course.save()
        return course

    @staticmethod
    def delete(course: Course) -> None:
        course.delete()


class LessonRepository:
    @staticmethod
    def get_by_course(course_id: int):
        return Lesson.objects.filter(course_id=course_id)

    @staticmethod
    def create(course, title: str, content: str, order: int) -> Lesson:
        return Lesson.objects.create(
            course=course,
            title=title,
            content=content,
            order=order
        )

class QuizRepository:
    @staticmethod
    def create(lesson, title: str) -> Quiz:
        return Quiz.objects.create(lesson=lesson, title=title)