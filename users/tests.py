from django.contrib.auth import get_user
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


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = User.objects.create_user(username='ismoiljon1', first_name='Ismoil', last_name='Mamirov')
        self.db_user.set_password('123456')
        self.db_user.save()
    def test_user_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                'username': 'ismoiljon1',
                'password': '123456'
            }
        )
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_user_logout(self):
        self.client.login(username='ismoiljon1', password='123456')
        self.client.get(reverse('users:logout'))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                'username': 'ismoil',
                'password': '123456'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                'username': 'ismoiljon1',
                'password': '1234'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):
    def test_user_login_required(self):
        response = self.client.get(
            reverse("users:profile"),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login') + "?next=/users/profile/")

    def test_profile_details(self):
        user = User.objects.create_user(username='ismoiljon1', first_name='Ismoil', last_name='Mamirov', email='ismoil@gmail.com')
        user.set_password('123456')
        user.save()

        self.client.login(username='ismoiljon1', password='123456')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.email)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)

    def test_update_user_profile(self):
        user = User.objects.create_user(username='ismoiljon1', first_name='Ismoil', last_name='Mamirov',
                                        email='ismoil@gmail.com')
        user.set_password('123456')
        user.save()

        self.client.login(username='ismoiljon1', password='123456')

        response = self.client.post(
            reverse('users:profile-edit'),
            data={
                'username': 'ismoiljon1',
                'first_name': 'Ismoilbek',
                'last_name': 'Abdulloh',
                'email': 'ismoil@gmail.com',
            }
        )
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Ismoilbek')
        self.assertEqual(user.last_name, 'Abdulloh')
        self.assertEqual(user.email, 'ismoil@gmail.com')
        self.assertEqual(response.url, reverse('users:profile'))
