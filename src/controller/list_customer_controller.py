from typing import Dict, List
from src.models.sqlite.interfaces.customer_repositor_interface import CustomerRepositoryInterface
from src.models.sqlite.entitites.customer import CustomerTable
from .interfaces.list_customer_controller_interfaces import ListCustomerControllerInterface

class ListCustomerController(ListCustomerControllerInterface):
    def __init__(self, customer_repository: CustomerRepositoryInterface) -> None:
        self.__customer_repository = customer_repository

    def list(self) -> Dict:
        self.__insert_customers_in_db()
        customer = self.__get_customer_in_db()
        response = self.__format_response(customer)
        return response
    
    def __insert_customers_in_db(self) -> None:
        self.__customer_repository.insert_customer()

    def __get_customer_in_db(self) -> List[CustomerTable]:
        customer = self.__customer_repository.get_all_customers()
        return customer
    
    def __format_response(self, customers: List[CustomerTable]) -> Dict:
        formatted_customers = []
        for customer in customers:
            formatted_customers.append({ "customer_description": customer.customer_description, "categoria_de_idade": customer.categoria_de_idade })
            
        return {
            "data": {
                "type": "Customers",
                "count": len(formatted_customers),
                "attributes": formatted_customers
            }
        }
