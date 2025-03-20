from abc import ABC, abstractmethod

class ListCustomerControllerInterface(ABC):

    @abstractmethod
    def list(self) -> dict:
        pass