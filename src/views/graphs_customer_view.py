from src.controller.customer_graph_controller import CustomerGraphController
from .interfaces.handle_graphs_interface import GraphsViewInterface
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse

class CustomerGraphsView(GraphsViewInterface):
    def __init__(self, controller: CustomerGraphController) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:  # Método renomeado para 'handle'
        response = self.__controller.prepare_customer_categories()
        return HttpResponse(status_code=200, body=response)
