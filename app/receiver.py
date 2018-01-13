class Receiver:
    """Abstract class describing the receiver.
    """

    def __init__(self, connection_params):
        self.timeout = 5
        self.finish = False
        self.connection_params = connection_params

    def start(self):
        raise NotImplementedError('Must be implemented!!!')

    def run(self):
        raise NotImplementedError('Must be implemented!!!')

    def stop(self):
        self.finish = True


class Postgres(Receiver):
    """Class realizing the receiving notifications from postgres db.
    """

    def start(self):
        pass

    def run(self):
        pass

    def stop(self):
        pass
