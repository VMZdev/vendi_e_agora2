from io import BytesIO
from base64 import b64encode
import matplotlib
from contextlib import contextmanager
from typing import Callable, Any
from matplotlib import pyplot as plt

@contextmanager
def safe_graph_context():
    """Context manager para criação segura de gráficos matplotlib"""
    original_backend = matplotlib.get_backend()
    matplotlib.use('Agg')
    
    try:
        yield plt
    finally:
        plt.close('all')
        matplotlib.use(original_backend)

def create_graph_image(plot_function: Callable[[Any], None], **kwargs) -> str:
    """
    Cria uma imagem de gráfico de forma segura
    
    Args:
        plot_function: Função que recebe o módulo plt como argumento
        **kwargs: Argumentos adicionais para a figura
        
    Returns:
        str: Imagem em base64
    """
    with safe_graph_context() as plt:
        plt.figure(figsize=kwargs.get('figsize', (8, 6)))
        plot_function(plt)
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        return f"data:image/png;base64,{b64encode(buffer.getvalue()).decode('utf-8')}"