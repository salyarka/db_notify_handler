class BaseAppException(Exception):
    """Base exception for app.
    """


class AppInitializationException(BaseAppException):
    """Raise when is troubles in
    app initialization.
    """


class DBException(BaseAppException):
    """Raise when is trouble in work with database.
    """
