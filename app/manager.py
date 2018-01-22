import threading

from queue import Queue

from config import get_config
from .receiver import Receiver
from .handler import Handler
from .worker import Pool


class Manager:

    def __init__(self, config_name):
        config = get_config(config_name)
        queue = Queue()
        self.__receiver = Receiver(config, queue)
        self.__handler = Handler(queue, Pool(config.WORKERS))

    def start(self):
        """Starts handler for handling messages from receiver and assign them
        to workers, and receiver for catching messages from db.
        """
        self.__handler = threading.Thread(target=self.__handler.start)
        self.__handler.start()
        self.__receiver.start()
