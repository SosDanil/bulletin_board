from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from ads.models import Ad, Review
from users.models import User


class UnauthorizedUserTestCase(APITestCase):
    """Класс для тестирования со стороны неавторизованного пользователя"""

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(pk=1, email='test@gmail.ru', phone=89504466999)
        self.ad = Ad.objects.create(pk=1, title='phone', price=10000, description='4 cameras', author=self.user)
        self.review = Review.objects.create(pk=1, ad=self.ad, author=self.user, text='good for this price')

    def test_ad_list(self):
        url = reverse('ads:ads_list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['results'][0]['title'],
            'phone'
        )

    def test_ad_retrieve(self):
        url = reverse('ads:ads_retrieve', args=(self.ad.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_ad_create(self):
        url = reverse('ads:ads_create')
        obj = {
            'title': 'car',
            'price': 500000
        }
        response = self.client.post(url, obj)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_ad_update(self):
        url = reverse('ads:ads_update', args=(self.ad.pk,))
        obj = {
            'price': 20000
        }
        response = self.client.patch(url, obj)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_ad_delete(self):
        url = reverse('ads:ads_delete', args=(self.ad.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_review_list(self):
        url = reverse('ads:reviews_list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data[0]['text'],
            'good for this price'
        )

    def test_review_retrieve(self):
        url = reverse('ads:reviews_retrieve', args=(self.review.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_review_create(self):
        url = reverse('ads:reviews_create')
        obj = {
            'text': 'test',
            'ad': self.ad
        }
        response = self.client.post(url, obj)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_review_update(self):
        url = reverse('ads:reviews_update', args=(self.review.pk,))
        obj = {
            'text': 'new test'
        }
        response = self.client.patch(url, obj)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_review_delete(self):
        url = reverse('ads:reviews_delete', args=(self.review.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class UserAuthorTestCase(APITestCase):
    """Класс для тестирования со стороны пользователя-автора"""

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(email='test@gmail.ru', phone=89504466999)
        self.ad = Ad.objects.create(title='phone', price=10000, description='4 cameras', author=self.user)
        self.review = Review.objects.create(ad=self.ad, author=self.user, text='good for this price')

        self.client.force_authenticate(user=self.user)

    def test_ad_list(self):
        url = reverse('ads:ads_list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['results'][0]['title'],
            'phone'
        )

    def test_ad_retrieve(self):
        url = reverse('ads:ads_retrieve', args=(self.ad.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['price'],
            10000
        )

    def test_ad_create(self):
        url = reverse('ads:ads_create')
        obj = {
            'title': 'car',
            'price': 500000,
        }
        response = self.client.post(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            data['price'],
            500000
        )

    def test_ad_update(self):
        url = reverse('ads:ads_update', args=(self.ad.pk,))
        obj = {
            'price': 20000
        }
        response = self.client.patch(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['price'],
            20000
        )

    def test_ad_delete(self):
        url = reverse('ads:ads_delete', args=(self.ad.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Ad.objects.all().count(),
            0
        )

    def test_review_list(self):
        url = reverse('ads:reviews_list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data[0]['text'],
            'good for this price'
        )

    def test_review_retrieve(self):
        url = reverse('ads:reviews_retrieve', args=(self.review.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['text'],
            self.review.text
        )

    def test_review_create(self):
        url = reverse('ads:reviews_create')
        obj = {
            'text': 'test',
            'ad': self.ad.pk
        }
        response = self.client.post(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            data['text'],
            'test'
        )

    def test_review_update(self):
        url = reverse('ads:reviews_update', args=(self.review.pk,))
        obj = {
            'text': 'new test'
        }
        response = self.client.patch(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['text'],
            'new test'
        )

    def test_review_delete(self):
        url = reverse('ads:reviews_delete', args=(self.review.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Review.objects.all().count(),
            0
        )


class UserNotAuthorTestCase(APITestCase):
    """Класс для тестирования со стороны пользователя, который не является автором товара и отзыва"""

    def setUp(self):
        self.client = APIClient()

        self.user_author = User.objects.create(email='test@gmail.ru', phone=89504466999)
        self.user_not_author = User.objects.create(email='test@yandex.ru', phone=89025070900)
        self.ad = Ad.objects.create(title='phone', price=10000, description='4 cameras', author=self.user_author)
        self.review = Review.objects.create(ad=self.ad, author=self.user_author, text='good for this price')

        self.client.force_authenticate(user=self.user_not_author)

    def test_ad_list(self):
        url = reverse('ads:ads_list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['results'][0]['title'],
            'phone'
        )

    def test_ad_retrieve(self):
        url = reverse('ads:ads_retrieve', args=(self.ad.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['price'],
            10000
        )

    def test_ad_create(self):
        url = reverse('ads:ads_create')
        obj = {
            'title': 'car',
            'price': 500000,
        }
        response = self.client.post(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            data['price'],
            500000
        )

    def test_ad_update(self):
        url = reverse('ads:ads_update', args=(self.ad.pk,))
        obj = {
            'price': 20000
        }
        response = self.client.patch(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            data['detail'],
            'Только автор или администратор может работать с объектом'
        )

    def test_ad_delete(self):
        url = reverse('ads:ads_delete', args=(self.ad.pk,))

        response = self.client.delete(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            Ad.objects.all().count(),
            1
        )
        self.assertEqual(
            data['detail'],
            'Только автор или администратор может работать с объектом'
        )

    def test_review_list(self):
        url = reverse('ads:reviews_list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data[0]['text'],
            'good for this price'
        )

    def test_review_retrieve(self):
        url = reverse('ads:reviews_retrieve', args=(self.review.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            data['detail'],
            'Только автор или администратор может работать с объектом'
        )

    def test_review_create(self):
        url = reverse('ads:reviews_create')
        obj = {
            'text': 'test',
            'ad': self.ad.pk
        }
        response = self.client.post(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            data['text'],
            'test'
        )

    def test_review_update(self):
        url = reverse('ads:reviews_update', args=(self.review.pk,))
        obj = {
            'text': 'new test'
        }
        response = self.client.patch(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            data['detail'],
            'Только автор или администратор может работать с объектом'
        )

    def test_review_delete(self):
        url = reverse('ads:reviews_delete', args=(self.review.pk,))

        response = self.client.delete(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            data['detail'],
            'Только автор или администратор может работать с объектом'
        )


class AdminTestCase(APITestCase):
    """Класс для тестирования со стороны пользователя, состоящего в группе администраторов"""

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(email='test@gmail.ru', phone=89504466999)
        self.user_admin = User.objects.create(email='admin@yandex.ru', phone=89025070900)
        self.ad = Ad.objects.create(title='phone', price=10000, description='4 cameras', author=self.user)
        self.review = Review.objects.create(ad=self.ad, author=self.user, text='good for this price')

        Group.objects.create(name='Администраторы')
        admin_group = Group.objects.get(name='Администраторы')
        admin_group.user_set.add(self.user_admin)

        self.client.force_authenticate(user=self.user_admin)

    def test_ad_list(self):
        url = reverse('ads:ads_list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['results'][0]['title'],
            'phone'
        )

    def test_ad_retrieve(self):
        url = reverse('ads:ads_retrieve', args=(self.ad.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['price'],
            10000
        )

    def test_ad_create(self):
        url = reverse('ads:ads_create')
        obj = {
            'title': 'car',
            'price': 500000,
        }
        response = self.client.post(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            data['price'],
            500000
        )

    def test_ad_update(self):
        url = reverse('ads:ads_update', args=(self.ad.pk,))
        obj = {
            'price': 20000
        }
        response = self.client.patch(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['price'],
            20000
        )

    def test_ad_delete(self):
        url = reverse('ads:ads_delete', args=(self.ad.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Ad.objects.all().count(),
            0
        )

    def test_review_list(self):
        url = reverse('ads:reviews_list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data[0]['text'],
            'good for this price'
        )

    def test_review_retrieve(self):
        url = reverse('ads:reviews_retrieve', args=(self.review.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['text'],
            self.review.text
        )

    def test_review_create(self):
        url = reverse('ads:reviews_create')
        obj = {
            'text': 'test',
            'ad': self.ad.pk
        }
        response = self.client.post(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            data['text'],
            'test'
        )

    def test_review_update(self):
        url = reverse('ads:reviews_update', args=(self.review.pk,))
        obj = {
            'text': 'new test'
        }
        response = self.client.patch(url, obj)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data['text'],
            'new test'
        )

    def test_review_delete(self):
        url = reverse('ads:reviews_delete', args=(self.review.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Review.objects.all().count(),
            0
        )
