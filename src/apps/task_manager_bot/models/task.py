
from django.db import models
from django.utils.translation import gettext


class Task(models.Model):

    # id = models.PositiveIntegerField(verbose_name=gettext('ID'), primary_key=True)
    user_id = models.PositiveBigIntegerField(verbose_name=gettext('ID Telegram'), db_index=True)
    date = models.DateField(verbose_name=gettext('Дата задачи'), default=0)
    start_datetime = models.TimeField(verbose_name=gettext('Время начала задачи'), default=0)
    end_datetime = models.TimeField(verbose_name=gettext('Время окончания задачи'), default=0)
    title = models.CharField(verbose_name=gettext('Название задачи'), max_length=150)
    description = models.TextField(verbose_name=gettext('Описание задачи'), default='')
    done = models.BooleanField(verbose_name=gettext('Выполенна задача'), default=None, null=True, blank=True)

    class Meta:
        verbose_name = 'Задача пользователя'
        verbose_name_plural = 'Задачи пользователей'
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['user_id', 'start_datetime', 'end_datetime', 'text'],
        #         name='unique_telegram_message')
        # ]
