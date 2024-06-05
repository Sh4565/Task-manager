
from django.db import models
from django.utils.translation import gettext


class Task(models.Model):

    user_id = models.PositiveBigIntegerField(verbose_name=gettext('ID Користувача'), db_index=True)
    date = models.DateField(verbose_name=gettext('Дата завдання'), default=0)
    start_datetime = models.TimeField(verbose_name=gettext('Час початку завдання'), default=0)
    end_datetime = models.TimeField(verbose_name=gettext('Час закінчення завдання'), default=0)
    title = models.CharField(verbose_name=gettext('Назва задачі'), max_length=150)
    description = models.TextField(verbose_name=gettext('Описание задачи'), default='')
    done = models.BooleanField(verbose_name=gettext('Виконане завдання'), default=None, null=True, blank=True)

    class Meta:
        verbose_name = gettext('Завдання користувача')
        verbose_name_plural = gettext('Завдання користувачів')
