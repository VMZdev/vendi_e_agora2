import pandas as pd
from io import BytesIO
from src.models.sqlite.interfaces.customer_repositor_interface import CustomerRepositoryInterface
from src.models.sqlite.entitites.customer import CustomerTable
from src.controller.interfaces.export_controller_interfaces import ExportControllerInterface

class ExportCustomerController(ExportControllerInterface):
    def __init__(self, customer_repository: CustomerRepositoryInterface) -> None:
        self.__customer_repository = customer_repository

    def export_to_excel(self) -> BytesIO:
        customers = self.__get_customer_in_db()
        df = self.__convert_to_dataframe(customers)
        output = self.__convert_df_to_excel_bytes(df)
        return output

    def __get_customer_in_db(self) -> list[CustomerTable]:
        return self.__customer_repository.get_all_customers()

    def __convert_to_dataframe(self, customers: list[CustomerTable]) -> pd.DataFrame:
        data = [
            {
                "customer_description": customer.customer_description,
                "categoria_de_idade": customer.categoria_de_idade
            }
            for customer in customers
        ]
        return pd.DataFrame(data)

    def __convert_df_to_excel_bytes(self, df: pd.DataFrame) -> BytesIO:
        output = BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        return output
