import gevent

from gevent.queue import Empty


class Handler:

    def __init__(self, queue):
        self.timeout = 5
        self.queue = queue
        self._thread = None

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
                with open('test_handler.txt', 'w') as fout:
                    fout.write('get notification')
                # task = self.create_task_from_notification(notification)
            # TODO app exception
            except:
                # TODO logging
                continue
            # self.task_handler.handle_task(task)

    def start(self):
        """Start catches notifications from queue.

        :return:
        """
        print('start in handler')
        self.__catch()
