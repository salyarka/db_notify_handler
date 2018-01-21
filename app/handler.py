from gevent.queue import Empty


class Handler:

    def __init__(self, queue, pool):
        self.timeout = 5
        self.queue = queue
        self._thread = None
        self.pool = pool

    def start(self):
        """Catches notifications from queue.
        """
        while True:
            try:
                notification = self.queue.get(timeout=self.timeout)
            except Empty:
                continue
            worker = self.pool.get()
            if worker is None:
                print('there are no free workers')
                continue
            worker.put_message(notification.payload)
