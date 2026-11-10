from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.courses.services import CourseService
from apps.courses.serializers import CourseSerializer, LessonSerializer
from .services import QuizService
from .serializers import QuizSerializer, QuizCreateSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse, Http404
from .services import CourseService
from drf_spectacular.utils import extend_schema
from .serializers import CourseCoverSerializer, CourseSerializer, LessonSerializer
from .jobs import get_job_status
from django.db.models import Count
from rest_framework import generics
from .models import Course
from .serializers import CourseSerializer
from .jobs import create_background_job

class CourseListCreateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CourseService()

    def get(self, request):
        courses = Course.objects.annotate(students_count=Count('enrollments')).order_by('created_at', 'id')
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            try:
                teacher = request.user if request.user.is_authenticated else None

                if not teacher:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    teacher = User.objects.first()
                    if not teacher:
                        return Response({"detail": "Спочатку створіть хоча б одного користувача/викладача"}, status=status.HTTP_400_BAD_REQUEST)

                course = self.service.create_course(
                    title=serializer.validated_data['title'],
                    description=serializer.validated_data['description'],
                    teacher=teacher
                )
                return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CourseService()

    def get(self, request, pk):
        course = self.service.get_course_details(pk)
        if not course:
            return Response({"detail": "Курс не знайдено"}, status=status.HTTP_404_NOT_FOUND)
        return Response(CourseSerializer(course).data)

    def put(self, request, pk):
        serializer = CourseSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            updated_course = self.service.update_course(pk, **serializer.validated_data)
            if not updated_course:
                return Response({"detail": "Курс не знайдено"}, status=status.HTTP_404_NOT_FOUND)
            return Response(CourseSerializer(updated_course).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        success = self.service.delete_course(pk)
        if not success:
            return Response({"detail": "Курс не знайдено"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CourseCoverView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CourseService()

    def get(self, request, pk):
        try:
            image_file = self.service.get_course_cover(pk)
            return FileResponse(image_file.open('rb'))
        except ValueError as e:
            raise Http404(str(e))

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'cover_image': {
                        'type': 'string',
                        'format': 'binary',
                    }
                },
                'required': ['cover_image'],
            }
        }
    )
    
    def post(self, request, pk):
        file_obj = request.FILES.get('cover_image')
        try:
            self.service.upload_course_cover(pk, file_obj)
            return Response({"detail": "Обкладинку успішно завантажено."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LessonCreateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CourseService()

    def post(self, request, course_id):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                lesson = self.service.add_lesson_to_course(
                    course_id=course_id,
                    title=data['title'],
                    content=data['content'],
                    order=data.get('order', 1)
                )
                return Response(LessonSerializer(lesson).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuizCreateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = QuizService()

    def post(self, request, lesson_id):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            try:
                quiz = self.service.create_quiz(
                    lesson_id=lesson_id,
                    title=serializer.validated_data['title']
                )
                return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobStatusView(APIView):
    def get(self, request, job_id):
        job_status = get_job_status(job_id)
        if not job_status:
            return Response({"detail": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"job_id": job_id, "status": job_status}, status=status.HTTP_200_OK)

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.annotate(students_count=Count('enrollments')).order_by('created_at', 'id')
    serializer_class = CourseSerializer

class CreateJobView(APIView):
    def post(self, request):
        job_id = create_background_job(request.data)
        return Response({"job_id": job_id, "status": "pending"}, status=status.HTTP_201_CREATED)