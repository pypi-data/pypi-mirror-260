from abc import ABC, abstractmethod


class IFlow(ABC):
    @abstractmethod
    def download(self, filekey):
        pass

    @abstractmethod
    def upload(self, filekey, fileName):
        pass
