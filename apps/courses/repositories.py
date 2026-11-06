from typing import List, Optional
from apps.courses.models import Course, Lesson


class CourseRepository:
    @staticmethod
    def get_all() -> List[Course]:
        return list(Course.objects.all())

    @staticmethod
    def get_by_id(course_id: int) -> Optional[Course]:
        return Course.objects.filter(id=course_id).first()

    @staticmethod
    def create(title: str, description: str, teacher_id: int) -> Course:
        return Course.objects.create(
            title=title,
            description=description,
            teacher_id=teacher_id,
        )


class LessonRepository:
    @staticmethod
    def get_by_course(course_id: int) -> List[Lesson]:
        return list(Lesson.objects.filter(course_id=course_id))