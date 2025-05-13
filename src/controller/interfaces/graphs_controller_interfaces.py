from abc import ABC, abstractmethod

class GraphsControllerInterface(ABC):

    @abstractmethod
    def list(self) -> dict:
        pass