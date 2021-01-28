import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "Discgolf is propably the best sport in the world"
    FLASK_DEBUG = True
    sources_root = os.path.abspath(os.path.dirname('App'))
    # todo prata i gruppen var vi vill lagra profilbilder.
    UPLOAD_FOLDER = os.path.join(sources_root, 'App/UI/static/assets/img/profile_pictures/')
