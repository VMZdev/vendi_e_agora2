from src.models.sqlite.entitites.products import ProductTable
from src.models.sqlite.interfaces.product_repository_interface import ProductRepositoryInterface
from src.functions.read_data import ReadDataController
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import exists, func
from pathlib import Path

class ProductRepository(ProductRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection
        base_path = Path(__file__).resolve().parent.parent.parent.parent.parent
        file_path = base_path / 'input_data.xlsx'        
        self.df_reader = ReadDataController(file_path=str(file_path))

    def insert_product(self) -> None:
        """Insere novos produtos no banco de dados, evitando duplicatas"""
        df = self.df_reader.read_excel()

        if df is not None and not df.empty:
            with self.__db_connection as database:
                try:
                    # Obtém o maior product_id atual
                    max_id = database.session.query(func.max(ProductTable.product_id)).scalar()
                    next_id = max_id + 1 if max_id is not None else 200000

                    for _, row in df.iterrows():
                        exists_query = (
                            database.session.query(exists().where(
                                ProductTable.product_description == row["product_description"]
                            ))
                            .scalar()
                        )

                        if not exists_query:
                            product_data = ProductTable(
                                product_id=next_id,  # ID manual sequencial
                                product_description=row["product_description"],
                                categoria_do_produto=row["product_category"]
                            )
                            database.session.add(product_data)
                            next_id += 1  # incrementa para o próximo produto

                    database.session.commit()
                except Exception as exception:
                    database.session.rollback()
                    raise exception

    def get_all_products(self) -> list[ProductTable]:
        with self.__db_connection as database:
            try:
                return database.session.query(ProductTable).all()
            except NoResultFound:
                return []
