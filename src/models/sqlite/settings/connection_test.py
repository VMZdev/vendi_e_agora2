import pytest
from sqlalchemy.engine import Engine
from .connection import db_connection_handler

# @pytest.mark.skip(reason="Interação com o banco") # Para Skippar um teste
def test_connect_to_db():
    assert db_connection_handler.get_engine() is None # Testar se o engine realmente é None

    db_connection_handler.connect_to_db()
    db_engine = db_connection_handler.get_engine()

    assert db_engine is not None # Depois de conectado, não vai ser None, ou seja, se por acaso o valor tiver mudado realmente o banco foi conectado
    assert isinstance(db_engine, Engine) # Verificar se eu tenho uma instância. Foi mesmo criada essa Engine?
