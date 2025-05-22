from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm, UserProfileForm
from django.core.files.uploadedfile import SimpleUploadedFile
import os

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'farsashraf44@gmail.com',
            'password': 'testpass123',
            'full_name': 'Test User'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_creation(self):
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.full_name, self.user_data['full_name'])
        self.assertTrue(self.user.check_password(self.user_data['password']))

    def test_user_str_method(self):
        self.assertEqual(str(self.user), self.user.email)

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.valid_data = {
            'email': 'farsashraf44@gmail.com',
            'full_name': 'New User',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }

    def test_registration_form_valid(self):
        form = UserRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'differentpass'
        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_registration_view(self):
        response = self.client.post(self.register_url, self.valid_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(email=self.valid_data['email']).exists())

class UserProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='farsashraf44@gmail.com',
            password='testpass123',
            full_name='Profile User'
        )
        self.client.login(email='farsashraf44@gmail.com', password='testpass123')
        self.profile_url = reverse('accounts:profile')

    def test_profile_view_authenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def test_profile_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_form_update(self):
        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # Empty file for testing
            content_type='image/jpeg'
        )
        form_data = {
            'full_name': 'Updated Name',
            'profile_image': test_image
        }
        form = UserProfileForm(data=form_data, files={'profile_image': test_image}, instance=self.user)
        self.assertTrue(form.is_valid())

class UserLoginLogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.user = User.objects.create_user(
            email='farsashraf44@gmail.com',
            password='testpass123'
        )

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'email': 'farsashraf44@gmail.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'email': 'farsashraf44@gmail.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page

    def test_logout(self):
        self.client.login(email='farsashraf44@gmail.com', password='testpass123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect after logout
