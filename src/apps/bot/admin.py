
from django.contrib import admin
from django.contrib.auth.models import User, Group

from apps.bot.models import TelegramUser, TelegramMessage


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(TelegramUser)
class BotUserAdmin(admin.ModelAdmin):

    list_display = ['user_id', 'username', 'first_name', 'last_name']
    list_filter = ['user_id', 'username', 'first_name', 'last_name']
    search_fields = ['user_id', 'username', 'first_name', 'last_name']
    readonly_fields = ['user_id', 'username', 'first_name', 'last_name']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(TelegramMessage)
class BotMessageAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'user_id', 'message_id', 'text', 'date']
    list_filter = ['chat_id', 'user_id', 'message_id', 'text', 'date']
    search_fields = ['chat_id', 'user_id', 'message_id', 'text', 'date']
    readonly_fields = ['chat_id', 'user_id', 'message_id', 'text', 'date']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
