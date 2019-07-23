import json


def load_config_from_json(filename, silent=False):
    try:
        with open(filename) as json_file:
            obj = json.loads(json_file.read())
            return obj
    except IOError as e:
        if silent:
            return False
        e.strerror = 'Unable to load configuration file (%s)' % e.strerror
        raise


class Config(object):
    DEBUG = True
    TESTING = True

    SECRET_KEY = '\xe6\x96\x1a\xa8z\xe8\xcb\\Uq\xf3\x08\xf47\xceTU\x0f\x92g\\\x91\xb5f'

    SESSION_COOKIE_SECURE = False
    PERMANENT_SESSION_LIFETIME = 1800

    GOOGLE_CLIENT_ID = '247405196335-73cc69ahvi69oeeojgj1giu6chrs59gj.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = 'sGmSa6Q2Vt6TgiYNghAnfl7_'
    OAUTH1_PROVIDER_ENFORCE_SSL = False

    SQLALCHEMY_DATABASE_URI = 'mysql://chatty_user:qwe90qwe@127.0.0.1/chatty'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    locals().update(
        load_config_from_json('/opt/chatty/conf/chatty.json', silent=True) or {})
