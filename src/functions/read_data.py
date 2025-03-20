import pandas as pd

class ReadDataController():
    def __init__(self, file_path):
        self.file_path = file_path

    def read_excel(self):
        try:
            # Lê o arquivo Excel
            df = pd.read_excel(self.file_path, dtype={"date": str})

            # Se houver valores NaT (valores nulos convertidos para Timestamp), convertemos para string vazia
            if "data" in df.columns:
                df["date"] = df["date"].astype(str)

            return df
        except Exception as e:
            print(f"Erro ao ler o arquivo Excel: {e}")
            return None
