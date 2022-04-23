from distutils.debug import DEBUG
import os

class Config(object):
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'onefelixe@gmail.com'
    MAIL_PASSWORD = 'dungmjgiiuyuwwot'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

class DevelopmentConfig(Config):
    DEBUG = False