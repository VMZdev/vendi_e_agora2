from unittest import mock
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entitites.customer import CustomerTable
from src.models.sqlite.repositories.customer_repository import CustomerRepository

#TESTE DO LIST
class MockConnection:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(CustomerTable)], #query
                    [
                        CustomerTable(customer_description="Clodoaldo", categoria_de_idade="dog"),
                     CustomerTable(customer_description="Greta", categoria_de_idade="cat")
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

def test_list_pets():
    mock_connection = MockConnection()
    repo = CustomerRepository(mock_connection)
    response = repo.get_all_customers()

    mock_connection.session.query.assert_called_once_with(CustomerTable) # Testando se é a PEts Table
    mock_connection.session.all.assert_called_once() # Testando se ta usando all()
    mock_connection.session.filter.assert_not_called() # Não há uso de filtro

    assert response[0].customer_description == "Clodoaldo"
