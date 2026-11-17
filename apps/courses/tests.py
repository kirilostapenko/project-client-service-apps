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

class JWTAuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')
        self.refresh_url = reverse('auth-refresh')
        self.logout_url = reverse('auth-logout')
        self.me_url = reverse('auth-me')
        self.courses_url = reverse('course-list-create')

        self.user_data = {
            'username': 'student_test',
            'email': 'student@example.com',
            'password': 'StrongPassword123'
        }

    def test_register_and_login_flow(self):
        reg_response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)

        login_response = self.client.post(self.login_url, {
            'username': 'student_test',
            'password': 'StrongPassword123'
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)
        self.assertIn('refresh', login_response.data)

    def test_protected_endpoint_without_token_returns_401(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_rotation_and_logout(self):
        self.client.post(self.register_url, self.user_data, format='json')
        login_res = self.client.post(self.login_url, {
            'username': 'student_test',
            'password': 'StrongPassword123'
        }, format='json')

        access_token = login_res.data['access']
        refresh_token = login_res.data['refresh']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        me_res = self.client.get(self.me_url)
        self.assertEqual(me_res.status_code, status.HTTP_200_OK)
        self.assertEqual(me_res.data['username'], 'student_test')

        refresh_res = self.client.post(self.refresh_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(refresh_res.status_code, status.HTTP_200_OK)
        new_refresh = refresh_res.data['refresh']
        new_access = refresh_res.data['access']

        old_refresh_res = self.client.post(self.refresh_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(old_refresh_res.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {new_access}')
        logout_res = self.client.post(self.logout_url, {'refresh': new_refresh}, format='json')
        self.assertEqual(logout_res.status_code, status.HTTP_204_NO_CONTENT)

        after_logout_refresh = self.client.post(self.refresh_url, {'refresh': new_refresh}, format='json')
        self.assertEqual(after_logout_refresh.status_code, status.HTTP_401_UNAUTHORIZED)