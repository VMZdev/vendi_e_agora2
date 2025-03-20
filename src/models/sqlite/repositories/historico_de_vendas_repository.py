from src.models.sqlite.entitites.historico_de_vendas import HistoricoDeVendasTable
from src.functions.read_data import ReadDataController
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.interfaces.historico_repository_interface import HistoricoRepositoryInterface

class HistoricoRepository(HistoricoRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection
        file_path = (
            r"C:\Users\victo\OneDrive\Documentos\OneDrive\Desktop\Projetos\VMZ Tecnologia\Cases\vendi_e_agora\input_data.xlsx"
        )
        self.df_reader = ReadDataController(file_path=file_path)

    def insert_historico(self) -> None:
        """Insere novos registros no banco de dados, evitando duplicatas"""
        df = self.df_reader.read_excel()  # Obtendo o DataFrame

        if df is not None and not df.empty:
            with self.__db_connection as database:
                try:
                    for _, row in df.iterrows():
                        historico_data = HistoricoDeVendasTable(
                            product_description=row["product_description"],
                            customer_description=row["customer_description"],
                            quantidade=row["quantity"],
                            valor=row["price"],
                            data=row["date"],
                        )
                        database.session.add(historico_data)

                    database.session.commit()
                except Exception as exception:
                    database.session.rollback()
                    raise exception


    def get_all_historico(self) -> list[HistoricoDeVendasTable]:
        """Recupera todos os registros da tabela HistoricoDeVendasTable"""
        with self.__db_connection as database:
            try:
                return database.session.query(HistoricoDeVendasTable).all()
            except NoResultFound:
                return []
