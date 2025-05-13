from src.controller.historico_graph_controller import HistoricoGraphController
from .interfaces.handle_graphs_interface import GraphsViewInterface
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse

class HistoricoGraphsView(GraphsViewInterface):
    def __init__(self, controller: HistoricoGraphController) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:  # Método renomeado para 'handle'
        response = self.__controller.prepare_historico_sales()
        return HttpResponse(status_code=200, body=response)