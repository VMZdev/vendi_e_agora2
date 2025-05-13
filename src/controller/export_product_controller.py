import pandas as pd
from io import BytesIO
from src.models.sqlite.interfaces.product_repository_interface import ProductRepositoryInterface
from src.models.sqlite.entitites.products import ProductTable
from src.controller.interfaces.export_controller_interfaces import ExportControllerInterface

class ExportProductController(ExportControllerInterface):
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.__product_repository = product_repository

    def export_to_excel(self) -> BytesIO:
        products = self.__get_product_in_db()
        df = self.__convert_to_dataframe(products)
        output = self.__convert_df_to_excel_bytes(df)
        return output

    def __get_product_in_db(self) -> list[ProductTable]:
        return self.__product_repository.get_all_products()

    def __convert_to_dataframe(self, products: list[ProductTable]) -> pd.DataFrame:
        data = [
            {
                "product_description": product.product_description,
                "categoria_do_produto": product.categoria_do_produto
            }
            for product in products
        ]
        return pd.DataFrame(data)

    def __convert_df_to_excel_bytes(self, df: pd.DataFrame) -> BytesIO:
        output = BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        return output
