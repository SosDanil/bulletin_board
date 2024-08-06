from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User


class UnauthorizedUserTestCase(APITestCase):
    """Класс для тестирования приложения users со стороны неавторизованного пользователя"""

    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru')

    def test_users_register(self):
        url = reverse('users:users_register')
        obj = {
            'email': 'danil@yandex.ru',
            'password': 'qwerty'
        }

        response = self.client.post(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            data['email'],
            'danil@yandex.ru'
        )

    def test_users_list(self):
        url = reverse('users:users_list')

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_users_retrieve(self):
        url = reverse('users:users_retrieve', args=(self.user.pk,))

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_users_update(self):
        url = reverse('users:users_update', args=(self.user.pk,))
        obj = {
            'phone': 89082550378
        }

        response = self.client.patch(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_users_delete(self):
        url = reverse('users:users_delete', args=(self.user.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_reset_password(self):
        url = reverse('users:reset_password')
        obj = {
            'email': 'sos.danil@yandex.ru'
        }

        response = self.client.post(url, obj)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class UserHimselfTestCase(APITestCase):
    """Класс для тестирования приложения users со стороны пользователя, который взаимодействует со своими данными"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@mail.ru', first_name='danil', phone=89006544321)

        self.client.force_authenticate(self.user)

    def test_users_register(self):
        url = reverse('users:users_register')
        obj = {
            'email': 'danil@yandex.ru',
            'password': 'qwerty'
        }

        response = self.client.post(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            data['email'],
            'danil@yandex.ru'
        )

    def test_users_register_same_email(self):
        url = reverse('users:users_register')
        obj = {
            'email': 'test@mail.ru',
            'password': 'qwerty'
        }

        response = self.client.post(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            data['email'],
            ['Пользователь с таким почта уже существует.']
        )

    def test_users_list(self):
        url = reverse('users:users_list')

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data[0]['first_name'],
            'danil'
        )

    def test_users_retrieve(self):
        url = reverse('users:users_retrieve', args=(self.user.pk,))

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['email'],
            'test@mail.ru'
        )

    def test_users_update(self):
        url = reverse('users:users_update', args=(self.user.pk,))
        obj = {
            'phone': 89082550378
        }

        response = self.client.patch(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['phone'],
            '89082550378'
        )

    def test_users_delete(self):
        url = reverse('users:users_delete', args=(self.user.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            User.objects.all().count(),
            0
        )

    def test_reset_password(self):
        url = reverse('users:reset_password')
        obj = {
            'email': 'sos.danil@yandex.ru'
        }

        response = self.client.post(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['message'],
            'Письмо отправлено на почту'
        )


class AlienUserTestCase(APITestCase):
    """Класс для тестирования приложения users со стороны пользователя, который взаимодействует НЕ со своими данными"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@mail.ru', first_name='danil', phone=89006544321)
        self.alien_user = User.objects.create(email='alien@mail.ru', first_name='kirill')

        self.client.force_authenticate(self.alien_user)

    def test_users_register(self):
        url = reverse('users:users_register')
        obj = {
            'email': 'danil@yandex.ru',
            'password': 'qwerty'
        }

        response = self.client.post(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            data['email'],
            'danil@yandex.ru'
        )

    def test_users_list(self):
        url = reverse('users:users_list')

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data[0]['first_name'],
            'danil'
        )

    def test_users_retrieve(self):
        url = reverse('users:users_retrieve', args=(self.user.pk,))

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_users_update(self):
        url = reverse('users:users_update', args=(self.user.pk,))
        obj = {
            'phone': 89082550378
        }

        response = self.client.patch(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_users_delete(self):
        url = reverse('users:users_delete', args=(self.user.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
