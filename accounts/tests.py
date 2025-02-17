from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsViewsTest(TestCase):
    def setUp(self):
        """Создание тестового пользователя"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.client = Client()

    def test_register_page_loads(self):
        """Проверка доступности страницы регистрации"""
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_successful_registration(self):
        """Проверка успешной регистрации"""
        url = reverse('register')
        response = self.client.post(url, {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('page_recipes'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_registration_with_empty_fields(self):
        """Попытка регистрации с пустыми полями"""
        url = reverse('register')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Обязательное поле.')

    def test_registration_with_short_password(self):
        """Попытка регистрации с коротким паролем"""
        url = reverse('register')
        response = self.client.post(url, {
            'username': 'shortpass',
            'password1': '123',
            'password2': '123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'слишком короткий')

    def test_registration_with_mismatched_passwords(self):
        """Попытка регистрации с несовпадающими паролями"""
        url = reverse('register')
        response = self.client.post(url, {
            'username': 'user2',
            'password1': 'complexpassword123',
            'password2': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'пароли не совпадают')

    def test_registration_with_existing_username(self):
        """Попытка регистрации с уже существующим именем пользователя"""
        url = reverse('register')
        response = self.client.post(url, {
            'username': 'testuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пользователь с таким именем уже существует')

    def test_login_page_loads(self):
        """Проверка доступности страницы входа"""
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        """Проверка успешного входа"""
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('page_recipes'))

    def test_failed_login_wrong_password(self):
        """Попытка входа с неправильным паролем"""
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверный логин или пароль')

    def test_failed_login_nonexistent_user(self):
        """Попытка входа несуществующего пользователя"""
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'nonexistent',
            'password': 'somepassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверный логин или пароль')

    def test_successful_logout(self):
        """Проверка успешного выхода"""
        self.client.login(username='testuser', password='testpassword123')
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('page_recipes'))
