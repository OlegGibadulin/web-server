from abc import ABC, abstractmethod

class BaseRequestHandler(ABC):
    @abstractmethod
    def handle(self, conn):
        pass
