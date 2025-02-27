from django.db import models

from users.models import User


class Course(models.Model):
    """
    Модель курса
    """
    title = models.CharField(max_length=200, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание курса')
    author = models.ForeignKey(User, verbose_name='Aвтор', null=True, blank=True, on_delete=models.CASCADE)
    preview = models.ImageField(upload_to='courses', null=True, blank=True, verbose_name='Превью курса')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    Модель урока
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    title = models.CharField(max_length=200, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока')
    author = models.ForeignKey(User, verbose_name='Aвтор', null=True, blank=True, on_delete=models.CASCADE)
    video_url = models.URLField(null=True, blank=True, verbose_name='Ссылка на видео')
    preview = models.ImageField(upload_to='lessons', null=True, blank=True, verbose_name='Превью урока')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class Subscribe(models.Model):
    """
    Модель подписки на курс
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Подписка: {self.user} - {self.course}"

    class Meta:
        unique_together = ['user', 'course']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'