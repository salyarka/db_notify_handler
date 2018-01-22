from multiprocessing import Process, Pipe


class Worker:

    def __init__(self, number):
        self.number = number
        self.is_busy = False
        self.__reader, self.__writer = Pipe()
        self.__process = None

    def __listen(self, writer):
        """Listens for the messages from the pipe.

        :param writer: pipe end
        :return:
        """
        while True:
            try:
                message = writer.recv()
            except EOFError:
                continue
            print('worker %s get message: %s' % (self.number, message))

    def start(self):
        """Spawns new process.
        """
        print('worker %s started' % self.number)
        self.__process = Process(
            target=self.__listen, args=(self.__writer,)
        )
        self.__process.start()

    def put_message(self, message):
        """Puts message to the pipe for process.

        :param message: message for worker
        :return:
        """
        self.__reader.send(message)
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
