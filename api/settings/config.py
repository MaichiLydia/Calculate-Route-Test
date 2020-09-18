import os

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'a_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    ENV = 'dev'
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY