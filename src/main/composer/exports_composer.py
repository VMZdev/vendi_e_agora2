from src.models.sqlite.settings.connection import db_connection_handler
from src.models.sqlite.repositories.customer_repository import CustomerRepository
from src.models.sqlite.repositories.products_repository import ProductRepository
from src.models.sqlite.repositories.historico_de_vendas_repository import HistoricoRepository

from src.controller.export_customer_controller import ExportCustomerController
from src.controller.export_product_controller import ExportProductController
from src.controller.export_historico_controller import ExportHistoricoController

from src.views.export_customer_view import ExportCustomerView
from src.views.export_product_view import ExportProductView
from src.views.export_historico_view import ExportHistoricoView

def exports_composer():
    # Instanciando os repositórios
    customer_repository = CustomerRepository(db_connection_handler)
    product_repository = ProductRepository(db_connection_handler)
    historico_repository = HistoricoRepository(db_connection_handler)

    # Instanciando os controladores
    customer_controller = ExportCustomerController(customer_repository)
    product_controller = ExportProductController(product_repository)
    historico_controller = ExportHistoricoController(historico_repository)

    # Instanciando as views
    customer_view = ExportCustomerView(customer_controller)
    product_view = ExportProductView(product_controller)
    historico_view = ExportHistoricoView(historico_controller)

    # Retornando todas as views agrupadas em um dicionário
    return {
        "customer_export_view": customer_view,
        "product_export_view": product_view,
        "historico_export_view": historico_view
    }
