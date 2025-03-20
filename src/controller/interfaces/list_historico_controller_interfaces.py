from abc import ABC, abstractmethod

class ListHistoricoControllerInterface(ABC):

    @abstractmethod
    def list(self) -> dict:
        pass
