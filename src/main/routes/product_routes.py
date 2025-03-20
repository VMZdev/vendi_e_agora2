from flask import Blueprint, jsonify
from src.views.http_types.http_request import HttpRequest
from src.main.composer.list_product_composer import list_product_composer 
from src.errors.error_handler import handle_errors

product_route_bp = Blueprint("product_routes", __name__)

@product_route_bp.route("/products", methods=["GET"])
def list_products():
    try:
        http_request = HttpRequest() # Vazio, pois a listagem não tem parametros
        view = list_product_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code