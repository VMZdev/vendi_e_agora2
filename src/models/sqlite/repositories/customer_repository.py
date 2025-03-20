from src.models.sqlite.entitites.customer import CustomerTable  
from src.models.sqlite.interfaces.customer_repositor_interface import CustomerRepositoryInterface
from src.functions.read_data import ReadDataController
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import exists

class CustomerRepository(CustomerRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection
        file_path = r'C:\Users\victo\OneDrive\Documentos\OneDrive\Desktop\Projetos\VMZ Tecnologia\Cases\vendi_e_agora\input_data.xlsx'
        self.df_reader = ReadDataController(file_path=file_path)

    def insert_customer(self) -> None:
        """Insere novos clientes no banco de dados, evitando duplicatas"""
        df = self.df_reader.read_excel()  # Obtendo o DataFrame

        if df is not None and not df.empty:
            with self.__db_connection as database:
                try:
                    for _, row in df.iterrows():
                        # Verifica se o cliente já existe no banco de dados
                        exists_query = (
                            database.session.query(exists().where(
                                CustomerTable.customer_description == ["customer_description"]
                            ))
                            .scalar()
                        )

                        if not exists_query:  # Se não existe, insere
                            customer_data = CustomerTable(
                                customer_description=row["customer_description"],  
                                categoria_de_idade=row["customer_category"]
                            )
                            database.session.add(customer_data)

                    database.session.commit()
                except Exception as exception:
                    database.session.rollback()
                    raise exception

    def get_all_customers(self) -> list[CustomerTable]:
        with self.__db_connection as database:
            try:
                customer = (database.session
                        .query(CustomerTable)
                        .all())
                return customer
            except NoResultFound:
                return []
