from src.models.sqlite.entitites.customer import CustomerTable  
from src.models.sqlite.interfaces.customer_repositor_interface import CustomerRepositoryInterface
from src.functions.read_data import ReadDataController
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import exists, func
from pathlib import Path

class CustomerRepository(CustomerRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection
        base_path = Path(__file__).resolve().parent.parent.parent.parent.parent  # sobe até a raiz do projeto
        file_path = base_path / 'input_data.xlsx'        
        self.df_reader = ReadDataController(file_path=str(file_path))

    def insert_customer(self) -> None:
        """Insere novos clientes no banco de dados, evitando duplicatas e garantindo que o primeiro ID seja 1000"""
        df = self.df_reader.read_excel()  # Obtendo o DataFrame

        if df is not None and not df.empty:
            with self.__db_connection as database:
                try:
                    # Verifica se a tabela está vazia
                    count_customers = database.session.query(func.count(CustomerTable.customer_id)).scalar()

                    for index, row in df.iterrows():
                        # Verifica se o cliente já existe no banco de dados
                        exists_query = (
                            database.session.query(exists().where(
                                CustomerTable.customer_description == row["customer_description"]
                            )) .scalar()
                        )

                        if not exists_query:  # Se não existe, insere
                            # Define o primeiro ID como 1000 se a tabela estiver vazia
                            customer_id = 1000 if count_customers == 0 and index == 0 else None

                            customer_data = CustomerTable(
                                customer_id=customer_id,  # Define o ID inicial apenas no primeiro registro
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
