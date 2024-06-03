# Generated by Django 5.0.6 on 2024-05-26 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveBigIntegerField(db_index=True, verbose_name='ID Telegram')),
                ('date', models.DateField(default=0, verbose_name='Дата задачи')),
                ('start_datetime', models.TimeField(default=0, verbose_name='Время начала задачи')),
                ('end_datetime', models.TimeField(default=0, verbose_name='Время окончания задачи')),
                ('text', models.TextField(null=True, verbose_name='Текст сообщения')),
                ('done', models.BinaryField()),
            ],
            options={
                'verbose_name': 'Задача пользователя',
                'verbose_name_plural': 'Задачи пользователей',
            },
        ),
        migrations.CreateModel(
            name='TelegramMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.PositiveBigIntegerField(db_index=True, verbose_name='ID Чата')),
                ('user_id', models.PositiveBigIntegerField(db_index=True, verbose_name='ID Telegram')),
                ('message_id', models.PositiveBigIntegerField(db_index=True, verbose_name='ID Сообщения')),
                ('text', models.TextField(null=True, verbose_name='Текст сообщения')),
                ('date', models.DateTimeField(default=0, verbose_name='Дата и время отправки сообщения')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveBigIntegerField(db_index=True, unique=True, verbose_name='ID Telegram')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=150, null=True, verbose_name='Фамилия')),
                ('username', models.CharField(max_length=150, null=True, verbose_name='Username')),
            ],
            options={
                'verbose_name': 'Пользователь бота',
                'verbose_name_plural': 'Пользователи бота',
            },
        ),
        migrations.AddConstraint(
            model_name='telegrammessage',
            constraint=models.UniqueConstraint(fields=('chat_id', 'user_id', 'message_id'), name='unique_telegram_message'),
        ),
    ]