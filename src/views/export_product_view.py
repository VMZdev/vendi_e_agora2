from src.controller.export_product_controller import ExportProductController
from src.views.interfaces.handle_export_interface import ExportViewInterface
from src.views.http_types.http_request import HttpRequest
from io import BytesIO

class ExportProductView(ExportViewInterface):
    def __init__(self, export_product_controller: ExportProductController) -> None:
        self.__export_product_controller = export_product_controller

    def handle_export(self, http_request: HttpRequest) -> BytesIO:
        try:
            return self.__export_product_controller.export_to_excel()
        except Exception as exception:
            raise Exception(f"Erro ao gerar o Excel de produtos: {str(exception)}")
