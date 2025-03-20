from src.models.sqlite.settings.connection import db_connection_handler # Dependência do Model abaixo no "db_connection_handler"
from src.models.sqlite.repositories.customer_repository import CustomerRepository
from src.controller.list_customer_controller import ListCustomerController
from src.views.list_customer_view import CustomerListerView

def list_customer_composer():
    model = CustomerRepository(db_connection_handler)
    controller = ListCustomerController(model)
    view = CustomerListerView(controller)

    return view
