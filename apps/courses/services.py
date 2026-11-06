from typing import List, Optional
from apps.courses.models import Course
from apps.courses.repositories import CourseRepository


class CourseService:
    def __init__(self, repository: CourseRepository = CourseRepository()):
        self.repository = repository

    def list_courses(self) -> List[Course]:
        return self.repository.get_all()

    def get_course_details(self, course_id: int) -> Optional[Course]:
        return self.repository.get_by_id(course_id)

    def create_new_course(self, title: str, description: str, teacher_id: int) -> Course:
        return self.repository.create(title, description, teacher_id)