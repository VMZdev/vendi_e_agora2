from src.models.sqlite.entitites.historico_de_vendas import HistoricoDeVendasTable
from src.functions.read_data import ReadDataController
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from src.models.sqlite.interfaces.historico_repository_interface import HistoricoRepositoryInterface
from pathlib import Path
from datetime import datetime

class HistoricoRepository(HistoricoRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection
        base_path = Path(__file__).resolve().parent.parent.parent.parent.parent
        file_path = base_path / 'input_data.xlsx'        
        self.df_reader = ReadDataController(file_path=str(file_path))

    def insert_historico(self) -> None:
        """Insere novos registros no banco de dados, com ID sequencial iniciando em 3000000"""
        df = self.df_reader.read_excel()

        if df is not None and not df.empty:
            with self.__db_connection as database:
                try:
                    max_id = database.session.query(func.max(HistoricoDeVendasTable.sale_id)).scalar()
                    next_id = max_id + 1 if max_id is not None else 3000000

                    for _, row in df.iterrows():
                        # Converter string para datetime.date
                        if isinstance(row["date"], str):
                            try:
                                data_obj = datetime.strptime(row["date"], "%Y-%m-%d").date()
                            except ValueError:
                                data_obj = None
                        else:
                            data_obj = row["date"]

                        historico_data = HistoricoDeVendasTable(
                            sale_id=next_id,
                            product_description=row["product_description"],
                            customer_description=row["customer_description"],
                            quantidade=row["quantity"],
                            valor=row["price"],
                            data=data_obj,
                        )
                        database.session.add(historico_data)
                        next_id += 1

                    database.session.commit()
                except Exception as exception:
                    database.session.rollback()
                    raise exception

    def get_all_historico(self) -> list[HistoricoDeVendasTable]:
        with self.__db_connection as database:
            try:
                return database.session.query(HistoricoDeVendasTable).all()
            except NoResultFound:
                return []
