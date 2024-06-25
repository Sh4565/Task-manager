
from .django import env, BASE_DIR, DEBUG


name = f'{env.str("MYSQL_DATABASE")}'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / f'{name}.sqlite3',
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env.str('MYSQL_DATABASE'),
            'USER': env.str('MYSQL_USER'),
            'PASSWORD': env.str('MYSQL_PASSWORD'),
            'HOST': env.str('DATABASE_HOST'),
            'PORT': env.str('DATABASE_PORT'),
        }
    }
