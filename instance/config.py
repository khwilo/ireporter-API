import os

class Config(object):
    """Parent configuration class"""
    DEBUG = False
    SECRET = os.getenv('SECRET_KEY')

class DevelopmentConfig(Config):
    """Configurations for development"""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for testing"""
    TESTING = True
    DEBUG = True

class StagingConfig(Config):
    """Configurations for staging"""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for production"""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
