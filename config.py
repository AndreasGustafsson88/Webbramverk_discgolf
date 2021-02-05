import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "Discgolf is propably the best sport in the world"
    FLASK_DEBUG = True
    MAX_CONTENT_LENGTH = 2024 * 2024
