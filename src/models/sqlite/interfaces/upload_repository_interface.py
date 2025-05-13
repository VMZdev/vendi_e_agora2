from typing import List, Optional, Dict, Any
from src.models.sqlite.entitites.uploads import UploadsTable
from src.models.sqlite.entitites.products import ProductTable
from src.models.sqlite.entitites.historico_de_vendas import HistoricoDeVendasTable
import pandas as pd

class UploadsRepositoryInterface:
    def add_upload(self, upload: UploadsTable) -> int:
        raise NotImplementedError
    
    def get_all_uploads(self) -> List[UploadsTable]:
        raise NotImplementedError
    
    def get_upload_by_id(self, upload_id: int) -> Optional[UploadsTable]:
        raise NotImplementedError
    
    def delete_upload(self, upload_id: int) -> bool:
        raise NotImplementedError
    
    def save_products(self, products: List[Dict[str, Any]]) -> int:
        raise NotImplementedError
    
    def save_sales_history(self, sales: List[Dict[str, Any]]) -> int:
        raise NotImplementedError
    
    def process_uploaded_file(self, file_path: str) -> Dict[str, int]:
        raise NotImplementedError