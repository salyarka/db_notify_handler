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
        gevent.spawn(self.handler.start)
        self.receiver.listen()
