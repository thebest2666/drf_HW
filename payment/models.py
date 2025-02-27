from django.db import models

from materials.models import Course, Lesson
from users.models import User


class Payment(models.Model):
    """
    Модель платежи
    """
    payment_choices = {
        'Cash': "Наличные",
        'Transfer': "Перевод ",
    }
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, verbose_name='Оплаченный курс', on_delete=models.CASCADE,null=True, blank=True)
    lesson = models.ForeignKey(Lesson, verbose_name='Оплаченный урок', on_delete=models.CASCADE, null=True, blank=True)
    payment_amount = models.PositiveIntegerField(default=0, verbose_name='Сумма оплаты')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    payment_method = models.CharField(max_length=250, choices=payment_choices, verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.user}: {self.course or self.lesson} = {self.payment_amount} руб.'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплата'