from os import environ

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '57e19ea558d4967a552d03deece34a70'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
