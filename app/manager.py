import threading

import gevent

from gevent.queue import Queue

from config import get_config
from .receiver import Receiver
from .handler import Handler


class Manager:

    def __init__(self, config_name):
        config = get_config(config_name)
        queue = Queue()
        self.receiver = Receiver(config, queue)
        self.handler = Handler(queue)
        self.workers = config.WORKERS

    def run(self):
        t1 = threading.Thread(target=self.handler.start)
        t2 = threading.Thread(target=self.receiver.listen)
        t1.start()
        t2.start()
        # gevent.spawn(self.handler.start)
        # self.receiver.listen()
