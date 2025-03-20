from abc import ABC, abstractmethod

class ListProductControllerInterface(ABC):

    @abstractmethod
    def list(self) -> dict:
        pass
