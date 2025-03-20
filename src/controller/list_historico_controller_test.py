import pytest
from src.models.sqlite.entitites.historico_de_vendas import HistoricoDeVendasTable
from src.controller.list_historico_controller import ListHistoricoController

# 🔹 Mock do Repositório com Dados Simulados (Ajustado para `get_all_historico`)
class MockHistoricoRepository:
    def insert_historico(self):
        """Simula a inserção de dados no banco de dados."""  # Apenas um mock, sem implementação real

    def get_all_historico(self):
        """Simula a obtenção de histórico de vendas do banco de dados."""
        return [
            HistoricoDeVendasTable(
                product_description="Produto A",
                customer_description="Carlos",
                quantidade=2,
                valor=100.0,
                data="2024-03-10"
            ),
            HistoricoDeVendasTable(
                product_description="Produto B",
                customer_description="Ana",
                quantidade=5,
                valor=250.0,
                data="2024-03-11"
            )
        ]

# 🔹 Teste da Formatação da Resposta
@pytest.mark.skip(reason="Interação com o banco")  # Para Skipping do teste se necessário
def test_list_historico():
    """Testa se a resposta formatada de list() está correta"""
    controller = ListHistoricoController(MockHistoricoRepository())

    # 🔹 Chamando o método correto (list)
    response = controller.list()

    # 🔹 Definição do formato esperado
    expected_response = {
        "data": {
            "type": "Historico",
            "count": 2,
            "attributes": [
                {
                    "product_description": "Produto A",
                    "customer_description": "Carlos",
                    "quantidade": 2,
                    "valor": 100.0,
                    "data": "2024-03-10"
                },
                {
                    "product_description": "Produto B",
                    "customer_description": "Ana",
                    "quantidade": 5,
                    "valor": 250.0,
                    "data": "2024-03-11"
                }
            ]
        }
    }

    # 🔹 Verificação se a resposta é exatamente como esperado
    assert response == expected_response
