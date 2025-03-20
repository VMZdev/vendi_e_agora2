from sqlalchemy import Column, String, Integer, REAL
from src.models.sqlite.settings.base import Base

class HistoricoDeVendasTable(Base):
    __tablename__ = "historico_de_vendas"

    sale_id = Column(Integer, primary_key=True)
    product_description = Column(String, nullable=False)
    customer_description = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor = Column(REAL, nullable=False)
    data = Column(String, nullable=False)

    def __repr__(self):
        return f"HistoricoDeVendas [product_description={self.product_description}, customer_description={self.customer_description}, quantidade={self.quantidade}, valor={self.valor}, data={self.data}]"
