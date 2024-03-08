import logging
import os
import random
import string
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from flask.logging import default_handler


def get_filename(app_name):
    if app_name is None:
        letters = string.ascii_lowercase
        app_name = ''.join(random.choice(letters) for i in range(10))
    filename = f"{app_name}.log"
    path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__name__)), f'logs'), f'{app_name}_logs')
    Path(path).mkdir(parents=True, exist_ok=True)
    return Path(path, filename)


def setup_logger(app):
    app.logger.removeHandler(default_handler)

    filename = get_filename(app.config.get('APP_NAME', 'general-microservices'))
    logging_handler = TimedRotatingFileHandler(filename, when="midnight", backupCount=30)
    logging_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(pathname)s, line %(lineno)d: %(message)s'
    ))
    logging.getLogger('werkzeug').addHandler(logging_handler)
    logging.getLogger(app.name).addHandler(logging_handler)
    logging.getLogger('gunicorn.error').addHandler(logging_handler)
    logging.getLogger('gunicorn.access').addHandler(logging_handler)
    app.logger.addHandler(logging_handler)
