from typing import List, Dict
from src.models.sqlite.interfaces.customer_repositor_interface import CustomerRepositoryInterface
from src.models.sqlite.entitites.customer import CustomerTable
from src.functions.graph_context import create_graph_image
from matplotlib import pyplot as plt
import matplotlib.patheffects

class CustomerGraphController:
    def __init__(self, customer_repository: CustomerRepositoryInterface) -> None:
        self.__customer_repository = customer_repository

    def prepare_customer_categories(self) -> Dict:
        customers = self.__customer_repository.get_all_customers()
        formatted_data = self.__format_customer_categories(customers)
        graph = self.__create_category_graph(formatted_data)
        return {"formatted_data": formatted_data, "graph": graph}

    def __format_customer_categories(self, customers: List[CustomerTable]) -> List[Dict]:
        categories = {}
        for customer in customers:
            age_category = customer.categoria_de_idade
            categories[age_category] = categories.get(age_category, 0) + 1
        
        return [{"age_category": k, "count": v} for k, v in categories.items()]

    def __create_category_graph(self, data: List[Dict]) -> str:
        def plot_function(plt):
            categories = [item["age_category"] for item in data]
            counts = [item["count"] for item in data]

            custom_colors = [
                "#eacf45",  # primary
                "#241f28",  # secondary
                "#16a085",  # accent
                "#fffced",  # text-like
                "#2980b9",  # opcional extra
                "#8e44ad",  # opcional extra
            ]

            fig, ax = plt.subplots(figsize=(8, 6), facecolor='none')  # remove fundo branco

            wedges, texts, autotexts = ax.pie(
                counts,
                labels=categories,
                autopct='%1.1f%%',
                startangle=140,
                colors=custom_colors[:len(categories)],
                textprops={'color': 'white', 'weight': 'bold'},
                wedgeprops={'edgecolor': 'black', 'linewidth': 1.5}
            )

            # Aplica contorno preto nas porcentagens
            for autotext in autotexts:
                autotext.set_path_effects([
                    plt.matplotlib.patheffects.Stroke(linewidth=1.5, foreground='black'),
                    plt.matplotlib.patheffects.Normal()
                ])

            ax.set_title("Categorias de Idade dos Clientes", color='white')
            ax.axis('equal')  # deixa o gráfico redondo

        return create_graph_image(plot_function, figsize=(8, 6))