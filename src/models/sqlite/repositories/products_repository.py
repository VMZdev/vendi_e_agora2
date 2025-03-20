from src.models.sqlite.entitites.products import ProductTable
from src.models.sqlite.interfaces.product_repository_interface import ProductRepositoryInterface
from src.functions.read_data import ReadDataController
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import exists

class ProductRepository(ProductRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection
        file_path = r'C:\Users\victo\OneDrive\Documentos\OneDrive\Desktop\Projetos\VMZ Tecnologia\Cases\vendi_e_agora\input_data.xlsx'
        self.df_reader = ReadDataController(file_path=file_path)

    def insert_product(self) -> None:
        """Insere novos produtos no banco de dados, evitando duplicatas"""
        df = self.df_reader.read_excel()  # Obtendo o DataFrame

        if df is not None and not df.empty:
            with self.__db_connection as database:
                try:
                    for _, row in df.iterrows():
                        # Verifica se o produto já existe no banco de dados
                        exists_query = (
                            database.session.query(exists().where(
                                ProductTable.product_description == row["product_description"]
                            ))
                            .scalar()
                        )

                        if not exists_query:  # Se não existe, insere
                            product_data = ProductTable(
                                product_description=row["product_description"],
                                categoria_do_produto=row["product_category"]
                            )
                            database.session.add(product_data)

                    database.session.commit()
                except Exception as exception:
                    database.session.rollback()
                    raise exception

    def get_all_products(self) -> list[ProductTable]:
        with self.__db_connection as database:
            try:
                product = (database.session
                        .query(ProductTable)
                        .all())
                return product
            except NoResultFound:
                return []
