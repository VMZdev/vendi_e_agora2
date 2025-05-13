from typing import Dict, List
from datetime import datetime
from src.models.sqlite.interfaces.historico_repository_interface import HistoricoRepositoryInterface
from src.models.sqlite.entitites.historico_de_vendas import HistoricoDeVendasTable
from .interfaces.list_historico_controller_interfaces import ListHistoricoControllerInterface

class ListHistoricoController(ListHistoricoControllerInterface):
    def __init__(self, historico_repository: HistoricoRepositoryInterface) -> None:
        self.__historico_repository = historico_repository

    def list(self) -> Dict:
        product = self.__get_historico_in_db()
        response = self.__format_response(product)
        return response

    def __get_historico_in_db(self) -> List[HistoricoDeVendasTable]:
        return self.__historico_repository.get_all_historico()

    def __format_response(self, historicos: List[HistoricoDeVendasTable]) -> Dict:
        formatted_historico = []
        for historico in historicos:
            raw_data = historico.data
            data_formatada = None

            # Tenta converter se for string
            if isinstance(raw_data, str):
                try:
                    raw_data = datetime.strptime(raw_data, "%Y-%m-%d")
                except ValueError:
                    try:
                        raw_data = datetime.strptime(raw_data, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        raw_data = None

            if raw_data:
                data_formatada = raw_data.strftime('%d/%m/%Y')

            formatted_historico.append({
                "product_description": historico.product_description,
                "customer_description": historico.customer_description,
                "quantidade": historico.quantidade,
                "valor": float(historico.valor),
                "data": data_formatada
            })

        return {
            "data": {
                "type": "Historico",
                "count": len(formatted_historico),
                "attributes": formatted_historico
            }
        }
