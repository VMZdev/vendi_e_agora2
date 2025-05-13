from typing import List, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import pandas as pd
import io
import logging
from src.models.sqlite.entitites.uploads import UploadsTable
from src.models.sqlite.entitites.products import ProductTable
from src.models.sqlite.entitites.customer import CustomerTable
from src.models.sqlite.entitites.historico_de_vendas import HistoricoDeVendasTable

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UploadsRepository:
    def __init__(self, db_connection):
        self.__db_connection = db_connection

    def add_upload_record(self, filename: str, file_size: int, file_type: str) -> int:
        """Adiciona um registro de upload na tabela uploads"""
        with self.__db_connection as db:
            try:
                new_upload = UploadsTable(
                    file_name=filename,
                    file_size=f"{file_size/1024:.2f} KB",
                    file_type=file_type,
                    upload_date=datetime.now()
                )
                db.session.add(new_upload)
                db.session.commit()
                return new_upload.upload_id
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Erro ao adicionar registro de upload: {str(e)}")
                raise Exception(f"Database error: {str(e)}")

    def process_excel_data(self, file) -> Dict[str, int]:
        """Processa o arquivo Excel e retorna estatísticas de importação"""
        filename = file.filename
        try:
            logger.info(f"Iniciando processamento do arquivo: {filename}")
            
            # Garantir que estamos no início do arquivo
            file.seek(0)
            file_content = file.read()
            
            # Verificação rigorosa do conteúdo
            if not file_content:
                logger.error("Arquivo sem conteúdo")
                raise ValueError("Arquivo está vazio (0 bytes)")

            if len(file_content) < 100:  # Tamanho mínimo para um arquivo Excel válido
                logger.error(f"Arquivo muito pequeno ({len(file_content)} bytes)")
                raise ValueError("Arquivo corrompido ou muito pequeno")

            # Verificar extensão
            file_ext = filename.split('.')[-1].lower()
            if file_ext not in ('xlsx', 'xls'):
                raise ValueError("Formato deve ser .xlsx ou .xls")

            # Determinar engine apropriado
            engine = 'openpyxl' if file_ext == 'xlsx' else 'xlrd'
            
            try:
                # Ler o arquivo Excel
                df = pd.read_excel(
                    io.BytesIO(file_content),
                    engine=engine,
                    dtype={
                        'customer_description': str,
                        'customer_category': str,
                        'product_description': str,
                        'product_category': str,
                        'quantity': 'Int64',  # Permite valores nulos
                        'price': float,
                        'date': str
                    }
                )
            except Exception as e:
                logger.error(f"Erro na leitura do Excel: {str(e)}")
                raise ValueError(f"Erro ao ler arquivo Excel: {str(e)}")

            # Verificar se o DataFrame tem dados
            if df.empty:
                raise ValueError("O arquivo Excel não contém dados")

            # Verificar colunas obrigatórias
            required_cols = {
                'customer_description', 'customer_category',
                'product_description', 'product_category',
                'quantity', 'price', 'date'
            }
            missing_cols = required_cols - set(df.columns)
            if missing_cols:
                raise ValueError(f"Colunas obrigatórias faltando: {', '.join(missing_cols)}")

            # Pré-processamento dos dados
            df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
            df = df.dropna(subset=['date', 'quantity', 'price'])
            
            # Processar os dados
            results = {
                'customers_saved': self._process_customers(df),
                'products_saved': self._process_products(df),
                'sales_saved': self._process_sales(df)
            }

            logger.info(f"Arquivo {filename} processado com sucesso. Resultados: {results}")
            return results

        except Exception as e:
            logger.error(f"Falha no processamento de {filename}: {str(e)}", exc_info=True)
            raise
        finally:
            file.seek(0)

    def _process_customers(self, df) -> int:
        """Processa e salva os clientes no banco de dados"""
        with self.__db_connection as db:
            try:
                # Obter clientes únicos
                customers = df[['customer_description', 'customer_category']].drop_duplicates()
                
                # Verificar clientes existentes
                existing = {c[0] for c in db.session.query(CustomerTable.customer_description).all()}
                
                # Preparar novos clientes
                new_customers = [
                    CustomerTable(
                        customer_description=row['customer_description'],
                        categoria_de_idade=row['customer_category']
                    )
                    for _, row in customers.iterrows()
                    if row['customer_description'] not in existing
                ]
                
                # Salvar no banco
                if new_customers:
                    db.session.bulk_save_objects(new_customers)
                    db.session.commit()
                
                return len(new_customers)
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Erro ao processar clientes: {str(e)}")
                raise

    def _process_products(self, df) -> int:
        """Processa e salva os produtos no banco de dados"""
        with self.__db_connection as db:
            try:
                # Obter produtos únicos
                products = df[['product_description', 'product_category']].drop_duplicates()
                
                # Verificar produtos existentes
                existing = {p[0] for p in db.session.query(ProductTable.product_description).all()}
                
                # Preparar novos produtos
                new_products = [
                    ProductTable(
                        product_description=row['product_description'],
                        categoria_do_produto=row['product_category']
                    )
                    for _, row in products.iterrows()
                    if row['product_description'] not in existing
                ]
                
                # Salvar no banco
                if new_products:
                    db.session.bulk_save_objects(new_products)
                    db.session.commit()
                
                return len(new_products)
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Erro ao processar produtos: {str(e)}")
                raise

    def _process_sales(self, df) -> int:
        """Processa e salva o histórico de vendas, evitando duplicatas"""
        with self.__db_connection as db:
            try:
                # Preparar dados de vendas
                sales_data = df.rename(columns={
                    'quantity': 'quantidade',
                    'price': 'valor',
                    'date': 'data'
                })[['product_description', 'customer_description', 'quantidade', 'valor', 'data']]

                new_sales = []
                for _, row in sales_data.iterrows():
                    exists = db.session.query(HistoricoDeVendasTable).filter_by(
                        product_description=row['product_description'],
                        customer_description=row['customer_description'],
                        quantidade=int(row['quantidade']),
                        valor=float(row['valor']),
                        data=row['data']
                    ).first()

                    if not exists:
                        new_sales.append(HistoricoDeVendasTable(
                            product_description=row['product_description'],
                            customer_description=row['customer_description'],
                            quantidade=int(row['quantidade']),
                            valor=float(row['valor']),
                            data=row['data']
                        ))

                if new_sales:
                    db.session.bulk_save_objects(new_sales)
                    db.session.commit()

                return len(new_sales)

            except Exception as e:
                db.session.rollback()
                logger.error(f"Erro ao processar vendas: {str(e)}")
                raise

    def get_upload_history(self) -> List[Dict[str, Any]]:
        """Obtém o histórico completo de uploads"""
        with self.__db_connection as db:
            try:
                uploads = db.session.query(UploadsTable).order_by(UploadsTable.upload_date.desc()).all()
                return [{
                    'id': upload.upload_id,
                    'name': upload.file_name,
                    'type': upload.file_type,
                    'size': upload.file_size,
                    'date': upload.upload_date.strftime("%Y-%m-%d %H:%M")
                } for upload in uploads]
            except SQLAlchemyError as e:
                logger.error(f"Erro ao buscar histórico: {str(e)}")
                raise Exception(f"Erro ao buscar histórico: {str(e)}")