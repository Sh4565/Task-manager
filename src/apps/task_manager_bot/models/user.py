
from django.db import models
from django.utils.translation import gettext


class TelegramUser(models.Model):
    """Пользователи телеграм бота"""

    language_choices = {
        'EN': 'English',
        'UA': 'Ukrainian',
        'RU': 'Russian',
    }

    user_id = models.PositiveBigIntegerField(verbose_name=gettext('ID Telegram'), db_index=True, unique=True)
    first_name = models.CharField(verbose_name=gettext('Имя'), max_length=150, null=False, blank=True)
    last_name = models.CharField(verbose_name=gettext('Фамилия'), max_length=150, null=True)
    username = models.CharField(verbose_name=gettext('Username'), max_length=150, null=True)
    utc = models.CharField(verbose_name=gettext('UTC'), max_length=3)
    language = models.CharField(verbose_name=gettext('Языковой интерфейс'), max_length=2, choices=language_choices)
    last_activity = models.DateTimeField(verbose_name=gettext('Последняя активность пользователя'))

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'
