from flask import Blueprint, jsonify, render_template, current_app
from jinja2 import TemplateNotFound
from src.main.composer.graph_composer import graphs_composer
from src.views.http_types.http_request import HttpRequest
from src.errors.error_handler import handle_errors
import os
from src.functions.auth_decorator import login_required

graphs_route_bp = Blueprint("graphs_routes", __name__)
views = graphs_composer()

@graphs_route_bp.route("/graph", methods=["GET"])
@login_required(role="dono")
def graph_page():
    try:
        # Debug opcional (pode remover depois)
        current_app.logger.debug(f"Procurando template em: {current_app.template_folder}")
        return render_template("graph.html")
    except TemplateNotFound as e:
        current_app.logger.error(f"Template não encontrado: {e}")
        raise
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@graphs_route_bp.route("/graph/customer", methods=["GET"])
@login_required(role="dono")
def customer_graph():
    try:
        http_request = HttpRequest()
        http_response = views["customer_view"].handle(http_request)
        
        # Renderiza o template com os dados do gráfico
        return render_template(
            "customer_graph.html",
            graph_data=http_response.body
        )
        
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@graphs_route_bp.route("/graph/product", methods=["GET"])
@login_required(role="dono")
def product_graph():
    try:
        http_request = HttpRequest()
        http_response = views["product_view"].handle(http_request)
        
        return render_template(
            "product_graph.html",
            graph_data=http_response.body
        )
        
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@graphs_route_bp.route("/graph/historico", methods=["GET"])
@login_required(role="dono")
def historico_graph():
    try:
        http_request = HttpRequest()
        http_response = views["historico_view"].handle(http_request)
        
        return render_template(
            "historico_graph.html",
            graph_data=http_response.body
        )
        
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code
