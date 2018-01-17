import os

from multiprocessing import Process, Pipe
from time import sleep


class Worker:

    def __init__(self):
        parent_conn, child_conn = Pipe()
        p = Process(target=self.__start, args=(child_conn,))
        p.start()

    def __start(self, conn):
        while True:
            print('worker, pid: %s; conn: %s' % (os.getpid(), conn))
            sleep(3)


class Pool:

    def __init__(self, workers_num):
        self.workers = [Worker() for each in range(workers_num)]

