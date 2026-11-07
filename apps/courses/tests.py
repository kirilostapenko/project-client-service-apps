from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Course

User = get_user_model()

class CourseFileIntegrationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teacher_test', password='password123')
        self.course = Course.objects.create(title='Course for Testing', teacher=self.user)
        self.url = reverse('course-cover', kwargs={'pk': self.course.pk})

    def test_upload_valid_png_cover(self):
        self.client.force_authenticate(user=self.user)
        png_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc`\x00\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82'
        uploaded_file = SimpleUploadedFile("cover.png", png_bytes, content_type="image/png")

        response = self.client.post(self.url, {'cover_image': uploaded_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        get_response = self.client.get(self.url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_upload_invalid_file_type_returns_bad_request(self):
        self.client.force_authenticate(user=self.user)
        txt_file = SimpleUploadedFile("notes.txt", b"some text content", content_type="text/plain")

        response = self.client.post(self.url, {'cover_image': txt_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)