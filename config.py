from distutils.debug import DEBUG
import os

class Config(object):
    MYSQL_HOST = 'remotemysql.com'
    MYSQL_USER = 'givcGg9Yql'
    MYSQL_PASSWORD = 'LHJOG3t1Ja'
    MYSQL_DB = 'givcGg9Yql'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'onefelixe@gmail.com'
    MAIL_PASSWORD = 'dungmjgiiuyuwwot'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    SECRET_KEY = b'\x1d\x8dle\x12\xf7\xfdO\x0b?\xe8\xbbZj"\x85'
    SESSION_TYPE = 'filesystem'
class DevelopmentConfig(Config):
    DEBUG = False