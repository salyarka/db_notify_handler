from config import get_config


class Manager:

    def __init__(self, config_name):
        config = get_config(config_name)
        self.receiver = config.RECEIVER
        self.receiver_uri = config.RECEIVER_URI
        self.workers = config.WORKERS

    def run(self):
        self.__start_workers()

    def __start_workers(self):
        print('receiver: %s' % self.receiver)
        print('receiver uri: %s' % self.receiver_uri)
        print('number of workers: %s' % self.workers)
