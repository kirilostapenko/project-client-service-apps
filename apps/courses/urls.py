from django.urls import path
from apps.courses.views import CourseListCreateView, CourseDetailView, LessonCreateView
from apps.courses.views import QuizCreateView
from .views import CourseCoverView
from .views import JobStatusView
from .views import CreateJobView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, CurrentUserView, LogoutView

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:course_id>/lessons/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:lesson_id>/quizzes/', QuizCreateView.as_view(), name='quiz-create'),
    path('courses/<int:pk>/cover/', CourseCoverView.as_view(), name='course-cover'),
    path('jobs/start/', CreateJobView.as_view(), name='start-job'),
    path('jobs/<str:job_id>/', JobStatusView.as_view(), name='job-status'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/me/', CurrentUserView.as_view(), name='auth-me'),
]