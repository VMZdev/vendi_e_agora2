import pytest
from src.models.sqlite.entitites.customer import CustomerTable
from src.controller.list_customer_controller import ListCustomerController

# 🔹 Mock do Repositório com Dados Simulados (Ajustado para `get_all_customers`)
class MockCustomersRepository:
    def get_all_customers(self):  # 🔥 Alterado de `list_customers()` para `get_all_customers()`
        return [
            CustomerTable(customer_description="Fluffy", categoria_de_idade="Cat"),
            CustomerTable(customer_description="Buddy", categoria_de_idade="Dog")
        ]

# 🔹 Teste da Formatação da Resposta
@pytest.mark.skip(reason="Interação com o banco") # Para Skippar um teste
def test_list_customers():
    """Testa se a resposta formatada de list() está correta"""
    controller = ListCustomerController(MockCustomersRepository())

    # 🔹 Chamando o método correto (list)
    response = controller.list()

    # 🔹 Definição do formato esperado
    expected_response = {
        "data": {
            "type": "Customers",
            "count": 2,
            "attributes": [
                { "customer_description": "Fluffy", "categoria_de_idade": "Cat"},
                { "customer_description": "Buddy", "categoria_de_idade": "Dog"}
            ]
        }
    }

    # 🔹 Verificação se a resposta é exatamente como esperado
    assert response == expected_response
