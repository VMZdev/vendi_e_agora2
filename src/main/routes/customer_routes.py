from flask import Blueprint, jsonify
from src.views.http_types.http_request import HttpRequest
from src.main.composer.list_customer_composer import list_customer_composer 
from src.errors.error_handler import handle_errors

customer_route_bp = Blueprint("customer_routes", __name__)

@customer_route_bp.route("/customers", methods=["GET"])
def list_customers():
    try:
        http_request = HttpRequest() # Vazio, pois a listagem não tem parametros
        view = list_customer_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code