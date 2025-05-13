from abc import ABC, abstractmethod
from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse

class ExportViewInterface(ABC):
    @abstractmethod
    def handle_export(self, http_request: HttpRequest) -> HttpResponse:
        pass
    