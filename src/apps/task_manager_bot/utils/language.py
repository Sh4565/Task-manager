
import csv
import logging

from pathlib import Path
from django.conf import settings


logger = logging.getLogger(__name__)


def get_language(code_text: str, language: str) -> str:
    # print(language)
    if language not in ['en', 'uk', 'ru']:
        language = 'en'

    locale_path = Path(settings.BASE_DIR, 'apps', 'task_manager_bot',
                       'locale', f'{language}.csv')

    with open(locale_path, encoding='utf-8') as f:
        data = csv.reader(f, delimiter='|')
        for i in data:
            if i[0] == code_text:
                logger.debug(f"{code_text}   {i[1]}")
                return i[1].replace('\\n', '\n')
