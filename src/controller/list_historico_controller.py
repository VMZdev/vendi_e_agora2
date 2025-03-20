from typing import Dict, List
from src.models.sqlite.interfaces.historico_repository_interface import HistoricoRepositoryInterface
from src.models.sqlite.entitites.historico_de_vendas import HistoricoDeVendasTable
from .interfaces.list_historico_controller_interfaces import ListHistoricoControllerInterface

class ListHistoricoController(ListHistoricoControllerInterface):
    def __init__(self, historico_repository: HistoricoRepositoryInterface) -> None:
        self.__historico_repository = historico_repository

    def list(self) -> Dict:
        self.__insert_historico_in_db()
        product = self.__get_historico_in_db()
        response = self.__format_response(product)
        return response
    
    def __insert_historico_in_db(self) -> None:
        self.__historico_repository.insert_historico()

    def __get_historico_in_db(self) -> List[HistoricoDeVendasTable]:
        historico = self.__historico_repository.get_all_historico()
        return historico
    
    def __format_response(self, historicos: List[HistoricoDeVendasTable]) -> Dict:
        formatted_historico = []
        for historico in historicos:
            formatted_historico.append({
            "product_description": historico.product_description,
            "customer_description": historico.customer_description,
            "quantidade": historico.quantidade,
            "valor": historico.valor,
            "data": historico.data
    })
        return {
            "data": {
                "type": "Historico",
                "count": len(formatted_historico),
                "attributes": formatted_historico
            }
        }
