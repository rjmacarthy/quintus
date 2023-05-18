import abc


class Loader(abc.ABC):
    def __init__(self, url):
        self.name = None
        self.url = url

    @abc.abstractmethod
    def run(self):
        pass
