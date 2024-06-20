from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class RegistrationTestCase(TestCase):
    def test_user_account_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                'username': 'ismoiljon1',
                'first_name': 'Ismoil',
                'last_name': 'Mamirov',
                'email': 'ismoil@gmail.com',
                'password': '123456',
            }
        )

        user = User.objects.get(username='ismoiljon1')
        self.assertEqual(user.first_name, 'Ismoil')
        self.assertEqual(user.last_name, 'Mamirov')
        self.assertEqual(user.email, 'ismoil@gmail.com')
        self.assertNotEqual(user.password, '123456')
        self.assertTrue(user.check_password('123456'))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                'first_name': 'Ismoil',
                'last_name': 'Mamirov',
            }
        )
        users_count = User.objects.count()
        self.assertEqual(users_count, 0)
        self.assertFormError(response.context.get('form'),'username', 'This field is required.')
        self.assertFormError(response.context.get('form'), 'password', 'This field is required.')

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                'username': 'ismoiljon1',
                'first_name': 'Ismoil',
                'last_name': 'Mamirov',
                'email': 'ismoil',
                'password': '123456',
            }
        )
        users_count = User.objects.count()
        self.assertEqual(users_count, 0)
        self.assertFormError(response.context.get('form'),'email', 'Enter a valid email address.')

    def test_unique_username(self):
        self.client.post(
            reverse("users:register"),
            data={
                'username': 'ismoiljon1',
                'first_name': 'Ismoil',
                'last_name': 'Mamirov',
                'email': 'ismoil@gmail.com',
                'password': '123456',
            }
        )
        users_count = User.objects.count()
        self.assertEqual(users_count, 1)

        response = self.client.post(
            reverse("users:register"),
            data={
                'username': 'ismoiljon1',
                'first_name': 'Ismoil',
                'last_name': 'Mamirov',
                'email': 'ismoil',
                'password': '123456',
            }

        )
        users_count = User.objects.count()
        self.assertEqual(users_count, 1)
        self.assertFormError(response.context.get('form'), 'username', 'A user with that username already exists.')