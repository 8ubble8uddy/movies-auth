from gevent import monkey

monkey.patch_all()

from secrets import token_hex

from flask import g, request

from manage import create_app

app = create_app()


@app.before_request
def before_request():
    """Функция для добавления в лог информации о `request-id`, с которым был выполнен запрос."""
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        request_id = token_hex(16)
    g.request_id = request_id
    app.logger.info('logging')
