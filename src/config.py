import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '57e19ea558d4967a552d03deece34a70'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    MONGO_URI = os.environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True
    MONGO_URI=os.environ.get('DATABASE_DEV_URL')

class TestConfig(Config):
    ENV="test"
    TESTING=True
    DEVELOPMENT=False
    DEBUG=False
    MONGO_URI=os.environ.get('DATABASE_TEST_URL')