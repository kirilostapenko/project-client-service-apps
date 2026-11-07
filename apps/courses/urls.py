from django.urls import path
from apps.courses.views import CourseListCreateView, CourseDetailView, LessonCreateView
from apps.courses.views import QuizCreateView
from .views import CourseCoverView

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:course_id>/lessons/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:lesson_id>/quizzes/', QuizCreateView.as_view(), name='quiz-create'),
    path('courses/<int:pk>/cover/', CourseCoverView.as_view(), name='course-cover'),
]