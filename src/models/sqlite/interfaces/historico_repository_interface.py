from abc import ABC, abstractmethod

class HistoricoRepositoryInterface(ABC):

    @abstractmethod
    def insert_historico(self) -> None:
        pass 

    @abstractmethod
    def get_all_historico(self) -> list:
        pass
