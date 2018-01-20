import gipc
import gevent


class Worker:

    def __init__(self, number):
        self.number = number
        self.reader, self.writer = gipc.pipe(duplex=True)
        self.process = None
        self._stop = False
        self.is_busy = False

    def start(self) -> None:
        """Spawns new process.

        :return:
        """
        print('worker %s started' % self.number)
        self.process = gipc.start_process(
            target=self.listen, args=(self.writer,)
        )

    def listen(self, writer) -> None:
        """Listens for the messages from the pipe.

        :param writer: pipe end
        :return:
        """
        while not self._stop:
            message = None
            with gevent.Timeout(5, False) as t:
                message = writer.get(timeout=t)
            if message is None:
                continue
            print('worker %s get message: %s' % (self.number, message))


class Pool:

    def __init__(self, workers_num):
        self.__workers = [Worker(num) for num in range(workers_num)]
        for worker in self.__workers:
            worker.start()

    def get(self) -> Worker:
        """Returns free worker.

        :return: worker
        """
        for worker in self.__workers:
            if not worker.is_busy:
                return worker
