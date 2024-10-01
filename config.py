# config.py
class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'SECRET_KEY'


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
