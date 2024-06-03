
import logging

from apps.task_manager_bot.main import scheduler
from .scheduler_users import add_users_scheduler


logger = logging.getLogger(__name__)


def init_scheduler():
    logger.debug('Проверяю наличие новых задач пользователей')
    scheduler.add_job(add_users_scheduler, 'interval', minutes=1)

    scheduler.start()
