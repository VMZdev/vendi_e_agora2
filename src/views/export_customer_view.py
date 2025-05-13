from src.controller.export_customer_controller import ExportCustomerController
from src.views.interfaces.handle_export_interface import ExportViewInterface
from src.views.http_types.http_request import HttpRequest
from io import BytesIO

class ExportCustomerView(ExportViewInterface):
    def __init__(self, export_customer_controller: ExportCustomerController) -> None:
        self.__export_customer_controller = export_customer_controller

    def handle_export(self, http_request: HttpRequest) -> BytesIO:
        try:
            # Chama o controller que retorna um arquivo Excel em memória
            excel_file = self.__export_customer_controller.export_to_excel()
            return excel_file
        except Exception as exception:
            raise Exception(f"Erro ao gerar o arquivo Excel: {str(exception)}")
