from src.models.sqlite.settings.connection import db_connection_handler # Dependência do Model abaixo no "db_connection_handler"
from src.models.sqlite.repositories.historico_de_vendas_repository import HistoricoRepository
from src.controller.list_historico_controller import ListHistoricoController
from src.views.list_historico_view import HistoricoListerView

def list_historico_composer():
    model = HistoricoRepository(db_connection_handler)
    controller = ListHistoricoController(model)
    view = HistoricoListerView(controller)

    return view
