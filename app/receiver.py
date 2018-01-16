import gevent

from gevent import monkey
from psycopg2 import connect

from .db.postgres_access import PostgresAccess


monkey.patch_all()


class Receiver:
    """Class that implements receiving of notifications from db.
    """

    def __init__(self, config, queue):
        self.timeout = 5
        self.__stop = False
        self.__conn = connect(config.DB_PARAMS['uri'])
        self.__db_params = config.DB_PARAMS
        self.__queue = queue

    def listen(self) -> None:
        """Starts listening notifications from db.

        :return:
        """
        with PostgresAccess(self.__db_params, self.__conn) as db:
            db.execute('LISTEN %s;' % self.__db_params['channel'].strip(';'))
            while not self.__stop:
                try:
                    gevent.socket.wait_read(
                        self.__conn.fileno(), timeout=self.timeout
                    )
                except gevent.socket.timeout:
                    # TODO add logging message
                    continue
                self.__conn.poll()
                while self.__conn.notifies:
                    notification = self.__conn.notifies.pop()
                    print('!!! notification', notification)
                    # TODO add logging message
                    self.__queue.put(notification)
                    print('!!! queue', self.__queue)
                    with open('test_receiver.txt', 'w') as fout:
                        fout.write(notification)

    def stop(self) -> None:
        """Stops listening db.

        :return:
        """
        self.__stop = True
