#!/bin/bash
postgres_ready() {
    $(which curl) http://${POSTGRES_HOST:-localhost}:${POSTGRES_PORT:-5432}/ 2>&1 | grep '52'
}

redis_ready() {
    exec 3<>/dev/tcp/${REDIS_HOST:-localhost}/${REDIS_PORT:-6379} && echo -e "PING\r\n" >&3 && head -c 7 <&3 | grep 'PONG'
}

until redis_ready; do
  >&2 echo 'Waiting for Redis to become available...'
  sleep 1
done
>&2 echo 'Redis is available.'

until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available.'

python manage.py migrate
gunicorn core.wsgi:app --bind 0.0.0.0:5000 -k gevent