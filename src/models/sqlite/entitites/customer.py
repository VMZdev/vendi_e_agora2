from sqlalchemy import Column, String, Integer
from src.models.sqlite.settings.base import Base

class CustomerTable(Base):
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True)
    customer_description = Column(String, nullable=False)
    categoria_de_idade = Column(String, nullable=False)

    def __repr__(self):
        return f"Customer [customer_description={self.customer_description}, categoria_de_idade={self.categoria_de_idade}]"