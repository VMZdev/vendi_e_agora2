from typing import List, Dict
from src.models.sqlite.interfaces.historico_repository_interface import HistoricoRepositoryInterface
from src.models.sqlite.entitites.historico_de_vendas import HistoricoDeVendasTable
from datetime import datetime
from src.functions.graph_context import create_graph_image
from matplotlib import pyplot as plt
import matplotlib.patheffects

class HistoricoGraphController:
    def __init__(self, historico_repository: HistoricoRepositoryInterface) -> None:
        self.__historico_repository = historico_repository

    def prepare_historico_sales(self) -> Dict:
        sales = self.__historico_repository.get_all_historico()
        formatted_data = self.__format_sales_data(sales)
        graph = self.__create_sales_graph(formatted_data)
        return {"formatted_data": formatted_data, "graph": graph}

    def __format_sales_data(self, sales: List[HistoricoDeVendasTable]) -> List[Dict]:
        from collections import defaultdict

        sales_by_month = defaultdict(float)
        date_labels = {}

        for item in sales:
            try:
                if isinstance(item.data, str):
                    date_obj = datetime.strptime(item.data.split()[0], "%Y-%m-%d")
                else:
                    date_obj = item.data

                date_key = datetime(date_obj.year, date_obj.month, 1)

                meses_pt = [
                    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
                ]
                label = f"{meses_pt[date_obj.month - 1]}/{date_obj.year}"

                sales_by_month[date_key] += item.valor
                date_labels[date_key] = label

            except Exception as e:
                print(f"Erro ao processar data {item.data}: {str(e)}")
                continue

        sorted_items = sorted(sales_by_month.items())
        return [{"month": date_labels[k], "total_sales": v} for k, v in sorted_items]

    def __create_sales_graph(self, data: List[Dict]) -> str:
        def plot_function(plt):
            from matplotlib import patheffects

            months = [item["month"] for item in data]
            total_sales = [item["total_sales"] for item in data]

            fig, ax = plt.subplots(figsize=(10, 6), facecolor='none')

            bars = ax.bar(months, total_sales, color="#eacf45", edgecolor="black", linewidth=1.5)

            for bar, value in zip(bars, total_sales):
                label = f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                height = bar.get_height()

                # Se for uma barra muito pequena, coloca o texto acima dela
                if height < 5:
                    y = height + 2
                    va = 'bottom'
                else:
                    y = height * 0.5
                    va = 'center'

                text = ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    y,
                    label,
                    ha='center',
                    va=va,
                    fontsize=10,
                    color="white",
                    weight="bold"
                )
                text.set_path_effects([
                    patheffects.Stroke(linewidth=1.5, foreground='black'),
                    patheffects.Normal()
                ])

            ax.set_title("Total de Vendas por Mês", color="white", fontsize=14, weight="bold")
            ax.set_xlabel("Mês", color="white")
            ax.set_ylabel("Total de Vendas (R$)", color="white")
            ax.tick_params(colors='white', rotation=45)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')

            plt.tight_layout()

        return create_graph_image(plot_function, figsize=(10, 6))
