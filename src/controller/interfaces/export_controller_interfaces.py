from abc import ABC, abstractmethod

class ExportControllerInterface(ABC):

    @abstractmethod
    def export_to_excel(self) -> None:
        pass