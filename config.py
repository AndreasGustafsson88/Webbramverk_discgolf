import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "Discgolf is propably the best sport in the world"
    FLASK_DEBUG = True
    MAX_CONTENT_LENGTH = 2024 * 2024
    MONGODB_URI = f'mongodb://root:password@localhost:27027'
    MONGODB_NAME = 'discgolf'


class TestConfig(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "Discgolf is propably the best sport in the world"
    FLASK_DEBUG = True
    MAX_CONTENT_LENGTH = 2024 * 2024
    WTF_CSRF_ENABLED = False
    MONGODB_URI = f'mongodb://root:password@localhost:27027'
    MONGODB_NAME = 'discgolf'


class LiveConfig(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "Discgolf is propably the best sport in the world"
    FLASK_DEBUG = False
    MAX_CONTENT_LENGTH = 2024 * 2024
    MONGODB_URI = f'mongodb+srv://gunicorn_user:s3cr37@cluster0.f9uyc.mongodb.net/discgolf?retryWrites=true&w=majority'
    MONGODB_NAME = 'discgolf'
