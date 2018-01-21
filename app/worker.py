import gipc
import gevent


class Worker:

    def __init__(self, number):
        self.number = number
        self.is_busy = False
        self.__reader, self.__writer = gipc.pipe(duplex=True)
        self.__process = None

    def __listen(self, writer):
        """Listens for the messages from the pipe.

        :param writer: pipe end
        :return:
        """
        while True:
            message = None
            with gevent.Timeout(5, False) as t:
                message = writer.get(timeout=t)
            if message is None:
                continue
            print('worker %s get message: %s' % (self.number, message))

    def start(self):
        """Spawns new process.
        """
        print('worker %s started' % self.number)
        self.__process = gipc.start_process(
            target=self.__listen, args=(self.__writer,)
        )

    def put_message(self, message):
        """Puts message to the pipe for process.

        :param message: message for worker
        :return:
        """
        self.__reader.put(message)
        self.is_busy = True


class Pool:

    def __init__(self, workers_num):
        self.__workers = [Worker(num) for num in range(workers_num)]
        for worker in self.__workers:
            worker.start()

    def get(self):
        """Returns free worker.

        :return: worker
        """
        for worker in self.__workers:
            if not worker.is_busy:
                return worker
