from src.controller.interfaces.graphs_controller_interfaces import GraphsControllerInterface
from .interfaces.handle_graphs_interface import GraphsViewInterface
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse

class ProductGraphsView(GraphsViewInterface):
    def __init__(self, controller: GraphsControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:  # ✅ Implementação correta
        graph_data = self.__controller.prepare_product_categories()
        return HttpResponse(status_code=200, body=graph_data)
