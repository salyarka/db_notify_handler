import os
import logging

from app.exceptions import AppInitializationException


class Base:
    """Base config.
    """
    DEBUG = False
    TESTING = False
    RECEIVER = os.environ.get('RECEIVER')
    RECEIVER_URI = os.environ.get('RECEIVER_URI')
    WORKERS = os.environ.get('WORKERS')

    @property
    def logging_level(self):
        """Abstract attribute,
        children must define their logging_level.
        """
        raise NotImplementedError('Must be implemented!!!')

    @classmethod
    def init_app(cls, app):
        """Initialize app with logging level.

        :param app: current app
        """
        if cls.RECEIVER is None:
            raise AppInitializationException(
                'Type of receiver is not defined!!!'
            )
        if cls.RECEIVER_URI is None:
            raise AppInitializationException(
                'Receiver URI is not defined!!!'
            )
        app.logger.setLevel(getattr(logging, cls.logging_level))


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


config = {
    'test': Test,
    'dev': Development,
    'prod': Production
}
