
from django.db import models
from django.utils.translation import gettext


class TelegramUser(models.Model):
    """Пользователи телеграм бота"""

    user_id = models.PositiveBigIntegerField(
        verbose_name=gettext('ID Telegram'),
        db_index=True,
        unique=True
    )
    username = models.CharField(
        verbose_name=gettext('Username'),
        max_length=150,
        blank=True,
        null=True
    )
    first_name = models.CharField(
        verbose_name=gettext('Имя'),
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        verbose_name=gettext('Фамилия'),
        max_length=150,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'


class TelegramMessage(models.Model):
    """Сообщения пользователей телеграм бота"""

    # user_id = models.ForeignKey(
    #     TelegramUser,
    #     verbose_name=gettext('Пользователи бота'),
    #     on_delete=models.CASCADE
    # )
    chat_id = models.PositiveBigIntegerField(
        verbose_name=gettext('ID Чата'),
        db_index=True,
    )
    user_id = models.PositiveBigIntegerField(
        verbose_name=gettext('ID Telegram'),
        db_index=True,
    )
    message_id = models.PositiveBigIntegerField(
        verbose_name=gettext('ID Сообщения'),
        db_index=True,
        default=0,
        null=False
    )
    text = models.CharField(
        verbose_name=gettext('Текст сообщения'),
        max_length=4096,
        blank=True,
        null=True
    )
    date = models.DateTimeField(
        verbose_name=gettext('Дата и время отправки сообщения'),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        constraints = [
            models.UniqueConstraint(fields=['chat_id', 'user_id', 'message_id'], name='unique_telegram_message')
        ]

    def __str__(self):
        return f'Chat: {self.chat_id}, User: {self.user_id}, Message: {self.message_id}, Text: {self.text}'