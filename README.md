## Practix Auth

[![python](https://img.shields.io/static/v1?label=python&message=3.8%20|%203.9%20|%203.10&color=informational)](https://github.com/8ubble8uddy/movies-auth/actions/workflows/main.yml)
[![dockerfile](https://img.shields.io/static/v1?label=dockerfile&message=published&color=2CB3E8)](https://hub.docker.com/r/8ubble8uddy/auth_api)
[![last updated](https://img.shields.io/static/v1?label=last%20updated&message=december%202022&color=yellow)](https://img.shields.io/static/v1?label=last%20updated&message=december%202022&color=yellow)
[![lint](https://img.shields.io/static/v1?label=lint&message=flake8%20|%20mypy&color=brightgreen)](https://github.com/8ubble8uddy/movies-auth/actions/workflows/main.yml)
[![code style](https://img.shields.io/static/v1?label=code%20style&message=WPS&color=orange)](https://wemake-python-styleguide.readthedocs.io/en/latest/)
[![tests](https://img.shields.io/static/v1?label=tests&message=%E2%9C%94%2023%20|%20%E2%9C%98%200&color=critical)](https://github.com/8ubble8uddy/movies-auth/actions/workflows/main.yml)

### **Описание**

_Целью данного проекта является реализация сервиса авторизации для онлайн-кинотеатра. В связи с этим были разработаны API для аутентификации и система управления ролями на основе фреймворка [Flask](https://flask.palletsprojects.com). Для хранения данных пользователей и истории входов используется реляционная база данных [PostgreSQL](https://www.postgresql.org). Аутентификация пользователей осуществляется с использованием JWT-токенов и с целью хранения недействительных access-токенов применяется [Redis](https://redis.io). Также в приложении реализованы: вход через социальные сервисы (протокол OAuth), распределённая трассировка для мониторинга (программа Jaeger) и Rate limit (ограничение количества запросов) от чрезмерной нагрузки сервера. Проект запускается через прокси-сервер [NGINX](https://nginx.org), который является точкой входа для веб-приложения. Ответы каждой ручки API покрыты тестами с помощью библиотеки [pytest](https://pytest.org)._

### **Технологии**

```Python``` ```Flask``` ```PostgreSQL``` ```Redis``` ```NGINX``` ```Gunicorn``` ```PyTest``` ```Docker```

### **Как запустить проект:**

Клонировать репозиторий и перейти внутри него в директорию ```/infra```:
```
git clone https://github.com/8ubble8uddy/movies-auth.git
```
```
cd movies-auth/infra/
```

Создать файл .env и добавить настройки для проекта:
```
nano .env
```
```
# PostgreSQL
POSTGRES_DB=users_database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
```

Развернуть и запустить проект в контейнерах:
```
docker-compose up
```

Документация API будет доступна по адресу:
```
http://127.0.0.1/openapi
```

### Автор: Герман Сизов