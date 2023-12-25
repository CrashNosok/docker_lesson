import abc


class MessageBroker(abc.ABC):
    @abc.abstractmethod
    def send(self, message):
        pass


class DatabaseStorage(abc.ABC):
    @abc.abstractmethod
    async def connect(self):
        pass

    @abc.abstractmethod
    async def save(self, data):
        pass

    @abc.abstractmethod
    async def find_news(self, reference):
        pass
