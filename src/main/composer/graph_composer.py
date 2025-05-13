from src.models.sqlite.settings.connection import db_connection_handler
from src.models.sqlite.repositories.customer_repository import CustomerRepository
from src.models.sqlite.repositories.products_repository import ProductRepository
from src.models.sqlite.repositories.historico_de_vendas_repository import HistoricoRepository

from src.controller.customer_graph_controller import CustomerGraphController
from src.controller.product_graph_controller import ProductGraphController
from src.controller.historico_graph_controller import HistoricoGraphController

from src.views.graphs_customer_view import CustomerGraphsView
from src.views.graphs_product_view import ProductGraphsView
from src.views.graphs_historico_view import HistoricoGraphsView

def graphs_composer():
    # Instanciando os repositórios
    customer_repository = CustomerRepository(db_connection_handler)
    product_repository = ProductRepository(db_connection_handler)
    historico_de_vendas_repository = HistoricoRepository(db_connection_handler)
    
    # Instanciando os controladores
    customer_controller = CustomerGraphController(customer_repository)
    product_controller = ProductGraphController(product_repository)
    historico_de_vendas_controller = HistoricoGraphController(historico_de_vendas_repository)
    
    # Instanciando as views
    customer_view = CustomerGraphsView(customer_controller)
    product_view = ProductGraphsView(product_controller)
    historico_de_vendas_view = HistoricoGraphsView(historico_de_vendas_controller)
    
    # Retornando todas as views
    return {
        "customer_view": customer_view,
        "product_view": product_view,
        "historico_view": historico_de_vendas_view
    }
