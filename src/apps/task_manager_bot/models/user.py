
from django.db import models
from django.utils.translation import gettext


class TelegramUser(models.Model):

    choices = {
        'en': 'English',
        'ua': 'Ukrainian',
        'ru': 'Russian',
    }

    user_id = models.PositiveBigIntegerField(verbose_name=gettext('ID Користувача'), db_index=True, unique=True)
    first_name = models.CharField(verbose_name=gettext("Ім'я"), max_length=150, null=False, blank=True)
    last_name = models.CharField(verbose_name=gettext('Прізвище'), max_length=150, null=True)
    username = models.CharField(verbose_name=gettext('Username'), max_length=150, null=True)
    timezone = models.CharField(verbose_name=gettext('UTC'), max_length=150, null=True)
    language = models.CharField(verbose_name=gettext('Мовний інтерфейс'), max_length=2, choices=choices, null=True)
    last_activity = models.DateTimeField(verbose_name=gettext('Остання активність користувача'), null=True)

    class Meta:
        verbose_name = gettext('Користувач бота')
        verbose_name_plural = gettext('Користувачі бота')
