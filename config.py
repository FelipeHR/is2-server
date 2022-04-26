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

class DevelopmentConfig(Config):
    DEBUG = False