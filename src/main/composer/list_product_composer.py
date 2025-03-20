from src.models.sqlite.settings.connection import db_connection_handler # Dependência do Model abaixo no "db_connection_handler"
from src.models.sqlite.repositories.products_repository import ProductRepository
from src.controller.list_product_controller import ListProductController
from src.views.list_product_view import ProductListerView

def list_product_composer():
    model = ProductRepository(db_connection_handler)
    controller = ListProductController(model)
    view = ProductListerView(controller)

    return view
