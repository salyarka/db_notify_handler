import os
# import logging

from app.exceptions import AppInitializationException


class Base:
    """Base config.
    """
    DEBUG = False
    TESTING = False
    DB_PARAMS = {
        'uri': os.environ.get('DB_URI'),
        'channel': os.environ.get('DB_CHANNEL'),
    }
    WORKERS = os.environ.get('WORKERS')

    def __init__(self):
        if self.DB_PARAMS['uri'] is None:
            raise AppInitializationException(
                'DB URI is not defined!!!'
            )
        if self.DB_PARAMS['channel'] is None:
            raise AppInitializationException(
                'DB CHANNEL is not defined!!!'
            )
        if self.WORKERS is None:
            raise AppInitializationException(
                'WORKERS number is not defined!!!'
            )
        self.WORKERS = int(self.WORKERS)
        # app.logger.setLevel(getattr(logging, cls.logging_level))

    @property
    def logging_level(self):
        """Abstract attribute,
        children must define their logging_level.
        """
        raise NotImplementedError('Must be implemented!!!')


class Test(Base):
    """Config for
    testing.
    """
    DEBUG = True
    TESTING = True
    logging_level = 'CRITICAL'


class Development(Base):
    """Config for
    development.
    """
    DEBUG = True
    logging_level = 'DEBUG'


class Production(Base):
    """Config for
    production.
    """
    logging_level = 'ERROR'
    # TODO Add SMTPHandler


config_map = {
    'test': Test,
    'dev': Development,
    'prod': Production
}


def get_config(config_name):
    try:
        return config_map[config_name]()
    except KeyError:
        raise AppInitializationException(
            'Unknown config name: %s.' % config_name
        )
