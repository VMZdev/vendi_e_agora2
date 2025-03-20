from unittest import mock
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
import pandas as pd
from src.models.sqlite.repositories.customer_repository import CustomerRepository
from src.functions.read_data import ReadDataController

#TESTE DO INSERT

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



    
# 🔹 Teste para Inserção de Clientes com Sucesso
@mock.patch.object(ReadDataController, 'read_excel')
def test_insert_customer(mock_read_excel):
    """Testa a inserção de clientes no banco"""
    mock_connection = MockConnection()
    repo = CustomerRepository(mock_connection)

    # Simula um DataFrame de clientes
    mock_read_excel.return_value = pd.DataFrame({
        "customer_description": ["Carlos", "Ana"],
        "categoria_de_idade": ["Idoso", "Adulto"]
    })

    repo.insert_customer()

    # 🔸 Verificações
    assert mock_connection.session.add.call_count == 2  # Deve ser chamado 2 vezes (para cada cliente)
    mock_connection.session.commit.assert_called_once()  # Deve chamar commit uma vez

# 🔹 Teste para Inserção sem Dados (DataFrame Vazio)
@mock.patch.object(ReadDataController, 'read_excel')
def test_insert_customer_no_data(mock_read_excel):
    """Testa a inserção quando o DataFrame está vazio"""
    mock_connection = MockConnection()
    repo = CustomerRepository(mock_connection)

    mock_read_excel.return_value = pd.DataFrame()  # DataFrame vazio

    repo.insert_customer()

    # 🔸 Verificações
    mock_connection.session.add.assert_not_called()  # Nenhuma inserção deve ser feita
    mock_connection.session.commit.assert_not_called()  # Nenhum commit deve ser feito

# 🔹 Teste para Erro ao Inserir Cliente (Erro na Conexão)
@mock.patch.object(ReadDataController, 'read_excel')
def test_insert_customer_error(mock_read_excel):
    """Testa erro ao tentar inserir clientes no banco"""
    mock_connection = MockConnectionNoResult()
    repo = CustomerRepository(mock_connection)

    # Simula um DataFrame de clientes
    mock_read_excel.return_value = pd.DataFrame({
        "customer_description": ["Carlos"],
        "categoria_de_idade": ["Idoso"]
    })

    with pytest.raises(Exception, match="Erro ao inserir no banco"):
        repo.insert_customer()

    # 🔸 Verificações
    mock_connection.session.rollback.assert_called_once()  # Deve chamar rollback no erro
