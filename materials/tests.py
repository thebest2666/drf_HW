from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscribe
from users.models import User


class LessonTestCase(APITestCase):
    """
    Тест для уроков
    """

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com')
        self.course = Course.objects.create(title='Test Course', description='Test Description', author=self.user)
        self.lesson = Lesson.objects.create(title='Test Lesson', description='Test Description', author=self.user,
                                            course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lessons_retrieve', args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.lesson.title
        )
        self.assertEqual(
            data['description'], self.lesson.description
        )
        self.assertEqual(
            data['course'], self.lesson.course.pk
        )
        self.assertEqual(
            data['author'], self.lesson.author.pk
        )

    def test_lesson_create(self):
        url = reverse('materials:lessons_create')
        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'course': self.course.pk,
            'author': self.user.pk
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(Lesson.objects.last().title, 'New Lesson')
        self.assertEqual(Lesson.objects.last().description, 'New Description')
        self.assertEqual(Lesson.objects.last().author, self.user)
        self.assertEqual(Lesson.objects.last().course, self.course)

    def test_lesson_update(self):
        url = reverse('materials:lessons_update', args=[self.lesson.pk])
        data = {
            'title': 'Updated Lesson',
            'description': 'Updated Description',
            'course': self.course.pk,
            'author': self.user.pk
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), 'Updated Lesson'
        )
        self.assertEqual(
            data.get('description'), 'Updated Description'
        )

    def test_lesson_delete(self):
        url = reverse('materials:lessons_delete', args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse('materials:lessons_list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['results'][0]['title'], self.lesson.title)
        self.assertEqual(data['results'][0]['description'], self.lesson.description)
        self.assertEqual(data['results'][0]['author'], self.lesson.author.pk)
        self.assertEqual(data['results'][0]['course'], self.lesson.course.pk)


class SubscribeToggleTestCase(APITestCase):
    """
    Тесты для подписки на курс
    """
    def setUp(self):
        self.user = User.objects.create(email='test_for_subscribe')
        self.course = Course.objects.create(title='Test Course', description='Test Description', author=self.user)
        self.subscribe = Subscribe.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse('materials:lessons_subscribe')
        data = {
            'course': self.course.pk
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Subscribe.objects.count(), 0)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Subscribe.objects.count(), 1)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Subscribe.objects.count(), 0)

