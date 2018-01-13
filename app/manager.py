from config import get_config
from .receiver import Receiver


class Manager:

    def __init__(self, config_name):
        config = get_config(config_name)
        self.receiver = Receiver(config)
        self.workers = config.WORKERS

    def run(self):
        self.__start_workers()

    def __start_workers(self):
        print('receiver: %s' % self.receiver)
        print('number of workers: %s' % self.workers)

    def __start_receiver(self):
        pass
