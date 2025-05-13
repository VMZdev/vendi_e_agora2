# src/functions/file_processor.py
from io import BytesIO
import pandas as pd
from werkzeug.datastructures import FileStorage
from typing import Tuple, Optional

class FileProcessor:
    @staticmethod
    def process_excel_file(file: FileStorage) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Process uploaded Excel file and return DataFrame with validation
        
        Args:
            file: Werkzeug FileStorage object from upload
            
        Returns:
            Tuple containing (DataFrame, error_message)
        """
        try:
            # Verify file is Excel
            if not file.filename.lower().endswith(('.xlsx', '.xls')):
                return None, "Invalid file type. Only Excel files are accepted"
            
            # Read file into memory
            excel_data = BytesIO(file.read())
            
            # Parse Excel with pandas
            df = pd.read_excel(excel_data)
            
            # Validate required columns
            required_columns = {'customer_description', 'customer_category'}
            if not required_columns.issubset(df.columns):
                missing = required_columns - set(df.columns)
                return None, f"Missing required columns: {', '.join(missing)}"
            
            return df, None
            
        except Exception as e:
            return None, f"Error processing file: {str(e)}"