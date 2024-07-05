# Task-manager

[![EN](https://img.shields.io/badge/lang-EN-blue.svg)](en.md)
[![RU](https://img.shields.io/badge/lang-RU-red.svg)](ru.md)

## About the project

This project is my thesis in which I explored the design of scalable Telegram bots with an admin panel.

## Deployment
___

### Cloning the repository

```shell
$ git clone 
```

### Setting up environment variables
Before starting the project, set up the environment variables in the .env file, based on the example .env.example.

### Setting up SSL
The ./.ssl/ directory should contain the fullchain.pem and privkey.pem files. You can obtain them using the command:

```shell
$ certbot --nginx
```

The obtained files will be located at /etc/letsencrypt/live/YOUR-DOMAIN/, where YOUR-DOMAIN is your registered domain name. Move the files to the .ssl directory:

```shell
cp /etc/letsencrypt/live/YOUR-DOMAIN/privkey.pem ./.ssl/privkey.pem
cp /etc/letsencrypt/live/YOUR-DOMAIN/fullchain.pem ./.ssl/fullchain.pem 
```

### Initializing and starting the project
Initialization and starting of the project are done with the command:

```shell
$ docker-compose up --build -d
```

### Running commands after the first start
The following commands are executed once after the first start:

```shell
$ docker-compose exec django python manage.py makemigrations
$ docker-compose exec django python manage.py migrate
$ docker-compose exec django python manage.py collectstatic --noinput
```
