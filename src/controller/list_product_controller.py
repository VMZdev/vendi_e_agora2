from typing import Dict, List
from src.models.sqlite.interfaces.product_repository_interface import ProductRepositoryInterface
from src.models.sqlite.entitites.products import ProductTable
from .interfaces.list_product_controller_interfaces import ListProductControllerInterface

class ListProductController(ListProductControllerInterface):
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.__product_repository = product_repository

    def list(self) -> Dict:
        self.__insert_product_in_db()
        product = self.__get_product_in_db()
        response = self.__format_response(product)
        return response
    
    def __insert_product_in_db(self) -> None:
        self.__product_repository.insert_product()

    def __get_product_in_db(self) -> List[ProductTable]:
        product = self.__product_repository.get_all_products()
        return product
    
    def __format_response(self, products: List[ProductTable]) -> Dict:
        formatted_products = []
        for product in products:
            formatted_products.append({ "product_description": product.product_description, "categoria_do_produto": product.categoria_do_produto }) # verificar
            
        return {
            "data": {
                "type": "Products",
                "count": len(formatted_products),
                "attributes": formatted_products
            }
        }
