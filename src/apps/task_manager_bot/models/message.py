
from django.db import models
from django.utils.translation import gettext


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
