import pytest
from src.models.sqlite.entitites.products import ProductTable
from src.controller.list_product_controller import ListProductController

# 🔹 Mock do Repositório com Dados Simulados (Ajustado para `get_all_customers`)
class MockProductsRepository:
    def get_all_products(self):  # 🔥 Alterado de `list_customers()` para `get_all_customers()`
        return [
            ProductTable(product_description="Fluffy", categoria_do_produto="Cat"),
            ProductTable(product_description="Buddy", categoria_do_produto="Dog")
        ]

# 🔹 Teste da Formatação da Resposta
@pytest.mark.skip(reason="Interação com o banco") # Para Skippar um teste
def test_list_products():
    """Testa se a resposta formatada de list() está correta"""
    controller = ListProductController(MockProductsRepository())

    # 🔹 Chamando o método correto (list)
    response = controller.list()

    # 🔹 Definição do formato esperado
    expected_response = {
        "data": {
            "type": "Products",
            "count": 2,
            "attributes": [
                { "product_description": "Fluffy", "categoria_do_produto": "Cat"},
                { "product_description": "Buddy", "categoria_do_produto": "Dog"}
            ]
        }
    }

    # 🔹 Verificação se a resposta é exatamente como esperado
    assert response == expected_response
