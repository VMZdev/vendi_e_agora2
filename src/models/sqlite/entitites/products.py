from sqlalchemy import Column, String, Integer
from src.models.sqlite.settings.base import Base

class ProductTable(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    product_description = Column(String, nullable=False)
    categoria_do_produto = Column(String, nullable=False)

    def __repr__(self):
        return f"Product [product_description={self.product_description}, categoria_do_produto={self.categoria_do_produto}]"