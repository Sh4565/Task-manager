
from django.db import models


class TelegramUser(models.Model):

    choices = {
        'en': 'English',
        'ua': 'Ukrainian',
        'ru': 'Russian',
    }

    user_id = models.PositiveBigIntegerField(verbose_name='ID Користувача', db_index=True, unique=True)
    first_name = models.CharField(verbose_name="Ім'я", max_length=150, null=False, blank=True)
    last_name = models.CharField(verbose_name='Прізвище', max_length=150, null=True)
    username = models.CharField(verbose_name='Username', max_length=150, null=True)
    timezone = models.CharField(verbose_name='UTC', max_length=150, null=True)
    language = models.CharField(verbose_name='Мовний інтерфейс', max_length=2, choices=choices, null=True)
    last_activity = models.DateTimeField(verbose_name='Остання активність користувача', null=True)

    class Meta:
        verbose_name = 'Користувач бота'
        verbose_name_plural = 'Користувачі бота'
