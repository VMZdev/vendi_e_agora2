from src.controller.interfaces.uploads_controller_interfaces import UploadsControllerInterface
from .interfaces.view_interface import ViewInterface
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse

class UploadsView(ViewInterface): # Trouxe a interface que obriga as views a implementar o método "handle"

    def __init__(self, controller: UploadsControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        body_response = self.__controller.list()
        return HttpResponse(status_code=200, body=body_response)