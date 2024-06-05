
from django.db import models
from django.utils.translation import gettext


class TelegramMessage(models.Model):

    chat_id = models.PositiveBigIntegerField(verbose_name=gettext('ID Чата'), db_index=True)
    user_id = models.PositiveBigIntegerField(verbose_name=gettext('ID Користувача'), db_index=True)
    message_id = models.PositiveBigIntegerField(verbose_name=gettext('ID Повідомлення'), db_index=True, null=False)
    text = models.TextField(verbose_name=gettext('Текст повідомлення'), null=True)
    date = models.DateTimeField(verbose_name=gettext('Дата та час надсилання повідомлення'), default=0)

    class Meta:
        verbose_name = gettext('Повідомлення')
        verbose_name_plural = gettext('Повідомлення')
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['chat_id', 'user_id', 'message_id'],
        #         name='unique_telegram_message')
        # ]
