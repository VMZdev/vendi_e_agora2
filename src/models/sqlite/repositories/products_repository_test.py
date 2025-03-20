from unittest import mock
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entitites.products import ProductTable
from src.models.sqlite.repositories.products_repository import ProductRepository

#TESTE DO LIST
class MockConnection:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(ProductTable)], #query
                    [
                        ProductTable(product_description="Clodoaldo", categoria_do_produto="dog"),
                     ProductTable(product_description="Greta", categoria_do_produto="cat")
                     ] # resultado
                       
                )
            ]
        )

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

class MockConnectionNoResult:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        self.session.query.side_effect = self.__raise_no_result_found

    def __raise_no_result_found(self, *args, **kwargs):
        raise NoResultFound("No result found")

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

def test_list_products():
    mock_connection = MockConnection()
    repo = ProductRepository(mock_connection)
    response = repo.get_all_products()

    mock_connection.session.query.assert_called_once_with(ProductTable) # Testando se é a Products Table
    mock_connection.session.all.assert_called_once() # Testando se ta usando all()
    mock_connection.session.filter.assert_not_called() # Não há uso de filtro

    assert response[0].product_description == "Clodoaldo"
