from gevent.queue import Empty


class Handler:

    def __init__(self, queue, pool):
        self.timeout = 5
        self.queue = queue
        self._thread = None
        self.pool = pool

    def __catch(self) -> None:
        """Catches notifications from queue.

        :return:
        """
        while True:
            try:
                notification = self.queue.get(timeout=self.timeout)
            except Empty:
                # TODO logging
                continue
            try:
                print('get notification: %s' % notification)
                worker = self.pool.get()
                if worker is None:
                    print('There are no free workers.')
                    continue
                worker.reader.put(notification.payload)
                # TODO is there a way to set is_busy in worker object???
                worker.is_busy = True
            # TODO app exception
            except Exception as e:
                # TODO logging
                print('except in handler: %s' % e)
                continue

    def start(self):
        """Start catches notifications from queue.

        :return:
        """
        print('start in handler')
        self.__catch()
