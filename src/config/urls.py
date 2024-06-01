
from django.contrib import admin
from django.urls import path

# from apps.TelegramBot.webhook import on_startup, on_shutdown

urlpatterns = [
    path('/', admin.site.urls),
    # path('set-webhook/', on_startup, name='set_webhook'),
    # path('delete-webhook/', on_shutdown, name='delete_webhook'),
]
