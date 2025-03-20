from abc import ABC, abstractmethod

class CustomerRepositoryInterface(ABC):

    @abstractmethod
    def insert_customer(self) -> None:
        pass 

    @abstractmethod
    def get_all_customers(self) -> list:
        pass
