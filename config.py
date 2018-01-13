import os
# import logging

from app.exceptions import AppInitializationException


class Base:
    """Base config.
    """
    DEBUG = False
    TESTING = False
    RECEIVER = os.environ.get('RECEIVER')
    RECEIVER_URI = os.environ.get('RECEIVER_URI')
    WORKERS = os.environ.get('WORKERS')

    def __init__(self):
        if self.RECEIVER is None:
            raise AppInitializationException(
                'Type of receiver is not defined!!!'
            )
        if self.RECEIVER_URI is None:
            raise AppInitializationException(
                'Receiver URI is not defined!!!'
            )
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
        return config_map[config_name]
    except KeyError:
        raise AppInitializationException(
            'Unknown config name: %s.' % config_name
        )
