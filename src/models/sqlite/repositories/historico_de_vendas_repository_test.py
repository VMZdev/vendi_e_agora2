from unittest import mock
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
import pandas as pd
from src.models.sqlite.repositories.historico_de_vendas_repository import HistoricoRepository
from src.functions.read_data import ReadDataController

# 🔹 Mock da Conexão com Banco de Dados (simula inserção bem-sucedida)
class MockConnection:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

# 🔹 Mock da Conexão que Simula Falha (simula erro na inserção)
class MockConnectionNoResult:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        self.session.add.side_effect = Exception("Erro ao inserir no banco")

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass


# 🔹 Teste para Inserção de Histórico de Vendas com Sucesso
@mock.patch.object(ReadDataController, 'read_excel')
def test_insert_historico(mock_read_excel):
    """Testa a inserção de históricos de vendas no banco"""
    mock_connection = MockConnection()
    repo = HistoricoRepository(mock_connection)

    # Simula um DataFrame de histórico de vendas
    mock_read_excel.return_value = pd.DataFrame({
        "customer_description": ["Carlos", "Ana"],
        "quantidade": [2, 5],
        "valor": [100.0, 250.0],
        "data": ["2024-03-10", "2024-03-11"],
        "sale_id": [1, 2],
        "product_description": ["Produto A", "Produto B"]
    })

    repo.insert_historico()

    # 🔸 Verificações
    assert mock_connection.session.add.call_count == 2  # Deve ser chamado 2 vezes (para cada venda)
    mock_connection.session.commit.assert_called_once()  # Deve chamar commit uma vez


# 🔹 Teste para Inserção sem Dados (DataFrame Vazio)
@mock.patch.object(ReadDataController, 'read_excel')
def test_insert_historico_no_data(mock_read_excel):
    """Testa a inserção quando o DataFrame está vazio"""
    mock_connection = MockConnection()
    repo = HistoricoRepository(mock_connection)

    mock_read_excel.return_value = pd.DataFrame()  # DataFrame vazio

    repo.insert_historico()

    # 🔸 Verificações
    mock_connection.session.add.assert_not_called()  # Nenhuma inserção deve ser feita
    mock_connection.session.commit.assert_not_called()  # Nenhum commit deve ser feito


# 🔹 Teste para Erro ao Inserir Histórico (Erro na Conexão)
@mock.patch.object(ReadDataController, 'read_excel')
def test_insert_historico_error(mock_read_excel):
    """Testa erro ao tentar inserir histórico de vendas no banco"""
    mock_connection = MockConnectionNoResult()
    repo = HistoricoRepository(mock_connection)

    # Simula um DataFrame de histórico de vendas
    mock_read_excel.return_value = pd.DataFrame({
        "customer_description": ["Carlos"],
        "quantidade": [2],
        "valor": [100.0],
        "data": ["2024-03-10"],
        "sale_id": [1],
        "product_description": ["Produto A"]
    })

    with pytest.raises(Exception, match="Erro ao inserir no banco"):
        repo.insert_historico()

    # 🔸 Verificações
    mock_connection.session.rollback.assert_called_once()  # Deve chamar rollback no erro
