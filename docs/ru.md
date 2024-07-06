# Task-manager

[![EN](https://img.shields.io/badge/lang-EN-blue.svg)](en.md)
[![RU](https://img.shields.io/badge/lang-RU-red.svg)](ru.md)

## О проекте
Данный проект является моим дипломом, в котором я рассмотрел проектирование масштабируемых телеграм ботов с админ панелью.

## Deployment
___

### Клонирование репозитория
```shell
$ git clone 
```

### Настройка переменных окружения
Перед запуском проекта нужно настроить переменные окружения в файле .env, опираясь на пример .env.example.

### Настройка SSL
В директории ./.ssl/ должны быть файлы fullchain.pem и privkey.pem. Их можно получить, используя команду:
```shell
$ certbot --nginx
```

Полученные файлы будут находиться по следующему пути: /etc/letsencrypt/live/YOUR-DOMAIN/, где YOUR-DOMAIN - ваше зарегистрированное доменное имя. Переместите файлы в директорию .ssl:

```shell
$ cp /etc/letsencrypt/live/YOUR-DOMAIN/privkey.pem ./.ssl/privkey.pem
$ cp /etc/letsencrypt/live/YOUR-DOMAIN/fullchain.pem ./.ssl/fullchain.pem 
```

### Инициализация и запуск проекта
Инициализация и запуск проекта выполняются при помощи команды:

```shell
$ docker-compose up --build -d
```

### Выполнение команд после первого запуска
Следующие команды выполняются один раз после первого запуска:

```shell
$ docker-compose exec django python manage.py makemigrations
$ docker-compose exec django python manage.py migrate
$ docker-compose exec django python manage.py collectstatic --noinput
```
