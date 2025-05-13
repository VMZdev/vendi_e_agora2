from typing import List, Dict
from src.models.sqlite.interfaces.product_repository_interface import ProductRepositoryInterface
from src.models.sqlite.entitites.products import ProductTable
from src.functions.graph_context import create_graph_image
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

class ProductGraphController:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.__product_repository = product_repository

    def prepare_product_categories(self) -> Dict:
        products = self.__product_repository.get_all_products()
        formatted_data = self.__format_product_categories(products)
        graph = self.__create_category_graph(formatted_data)
        return {"formatted_data": formatted_data, "graph": graph}

    def __format_product_categories(self, products: List[ProductTable]) -> List[Dict]:
        categories = {}
        for product in products:
            category = product.categoria_do_produto
            categories[category] = categories.get(category, 0) + 1
        
        return [{"category": k, "count": v} for k, v in categories.items()]

    def __create_category_graph(self, data: List[Dict]) -> str:
        def plot_function(plt):
            from matplotlib import patheffects

            categories = [item["category"] for item in data]
            counts = [item["count"] for item in data]

            fig, ax = plt.subplots(figsize=(10, 6), facecolor='none')

            bars = ax.bar(
                categories,
                counts,
                color="#eacf45",
                edgecolor="black",
                linewidth=1.5
            )

            # Remover labels nas barras (não adiciona textos)

            ax.set_title("Distribuição por Categoria de Produto", color="white", fontsize=14, weight="bold")
            ax.set_xlabel("Categoria", color="white")
            ax.set_ylabel("Quantidade", color="white")
            ax.tick_params(colors='white', rotation=45)

            # Ajusta o eixo Y para apenas inteiros
            ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

            # Estética das bordas
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')

            plt.tight_layout()

        return create_graph_image(plot_function, figsize=(10, 6))
