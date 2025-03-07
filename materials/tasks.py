import datetime

import pytz
from celery import shared_task
from django.core.mail import send_mail
from config.settings import DEFAULT_FROM_EMAIL, TIME_ZONE
from materials.models import Subscribe
from users.models import User


TIME_DELTA_LAST_LOGIN = datetime.timedelta(days=30)
ZONE = pytz.timezone(TIME_ZONE)


@shared_task
def send_mail_after_course_update():
    subscriptions = Subscribe.objects.all()
    subscriptions_list = []
    for subscription in subscriptions:
        subscriptions_list.append(subscription.user.email)
    send_mail(
        "Вышел новый урок", "По курсу из Вашей подписки появился новый урок!", DEFAULT_FROM_EMAIL, subscriptions_list
    )

@shared_task
def block_inactive_users():
    users = User.objects.filter(is_active=True)
    current_date = datetime.datetime.now(ZONE)
    for user in users:
        if user.last_login:
            if user.last_login + TIME_DELTA_LAST_LOGIN < current_date:
                user.is_active = False
                user.save()
        else:
            if user.date_joined + TIME_DELTA_LAST_LOGIN < current_date:
                user.is_active = False
                user.save()