from abc import ABC, abstractmethod


class IProcessor(ABC):
    @abstractmethod
    def run(self):
        pass
    
    @abstractmethod
    def uploadStats(self):
        pass

    @abstractmethod
    def close(self):
        pass