import gevent

from gevent import monkey
from psycopg2 import connect

from .db.postgres_access import PostgresAccess


monkey.patch_all()


class Receiver:
    """Class that implements receiving of notifications from db.
    """

    def __init__(self, config, queue):
        self.__timeout = 5
        self.__stop = False
        self.__conn = connect(config.DB_PARAMS['uri'])
        self.__db_params = config.DB_PARAMS
        self.__queue = queue

    def start(self):
        """Starts listening notifications from db.
        """
        with PostgresAccess(self.__conn) as db:
            db.execute('LISTEN %s;' % self.__db_params['channel'].strip(';'))
            while not self.__stop:
                try:
                    gevent.socket.wait_read(
                        self.__conn.fileno(), timeout=self.__timeout
                    )
                except gevent.socket.timeout:
                    continue
                self.__conn.poll()
                while self.__conn.notifies:
                    notification = self.__conn.notifies.pop()
                    print('received notification: %s' % notification)
                    self.__queue.put(notification)
