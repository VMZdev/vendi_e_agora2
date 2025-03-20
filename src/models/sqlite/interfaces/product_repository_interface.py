from abc import ABC, abstractmethod

class ProductRepositoryInterface(ABC):

    @abstractmethod
    def insert_product(self) -> None:
        pass 

    @abstractmethod
    def get_all_products(self) -> list:
        pass
