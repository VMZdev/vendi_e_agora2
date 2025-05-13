import pandas as pd
from io import BytesIO
from src.models.sqlite.interfaces.historico_repository_interface import HistoricoRepositoryInterface
from src.models.sqlite.entitites.historico_de_vendas import HistoricoDeVendasTable
from src.controller.interfaces.export_controller_interfaces import ExportControllerInterface

class ExportHistoricoController(ExportControllerInterface):
    def __init__(self, historico_repository: HistoricoRepositoryInterface) -> None:
        self.__historico_repository = historico_repository

    def export_to_excel(self) -> BytesIO:
        historico = self.__get_historico_in_db()
        df = self.__convert_to_dataframe(historico)
        output = self.__convert_df_to_excel_bytes(df)
        return output

    def __get_historico_in_db(self) -> list[HistoricoDeVendasTable]:
        return self.__historico_repository.get_all_historico()

    def __convert_to_dataframe(self, historicos: list[HistoricoDeVendasTable]) -> pd.DataFrame:
        data = [
            {
                "product_description": h.product_description,
                "customer_description": h.customer_description,
                "quantidade": h.quantidade,
                "valor": float(h.valor),
                "data": h.data
            }
            for h in historicos
        ]
        return pd.DataFrame(data)

    def __convert_df_to_excel_bytes(self, df: pd.DataFrame) -> BytesIO:
        output = BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        return output
