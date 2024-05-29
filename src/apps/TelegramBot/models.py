
from django.db import models
from django.utils.translation import gettext


class TelegramUser(models.Model):
    """Пользователи телеграм бота"""

    user_id = models.PositiveBigIntegerField(verbose_name=gettext('ID Telegram'), db_index=True, unique=True)
    first_name = models.CharField(verbose_name=gettext('Имя'), max_length=150, null=False, blank=True)
    last_name = models.CharField(verbose_name=gettext('Фамилия'), max_length=150, null=True)
    username = models.CharField(verbose_name=gettext('Username'), max_length=150, null=True)

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'


class TelegramMessage(models.Model):
    """Сообщения пользователей телеграм бота"""

    chat_id = models.PositiveBigIntegerField(verbose_name=gettext('ID Чата'), db_index=True)
    user_id = models.PositiveBigIntegerField(verbose_name=gettext('ID Telegram'), db_index=True)
    message_id = models.PositiveBigIntegerField(verbose_name=gettext('ID Сообщения'), db_index=True, null=False)
    text = models.TextField(verbose_name=gettext('Текст сообщения'), null=True)
    date = models.DateTimeField(verbose_name=gettext('Дата и время отправки сообщения'), default=0)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        constraints = [
            models.UniqueConstraint(
                fields=['chat_id', 'user_id', 'message_id'],
                name='unique_telegram_message')
        ]

    def __str__(self):
        return f'Chat: {self.chat_id}, User: {self.user_id}, Message: {self.message_id}, Text: {self.text}'


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
