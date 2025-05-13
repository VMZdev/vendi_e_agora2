from flask import Blueprint, jsonify, render_template
from src.views.http_types.http_request import HttpRequest
from src.main.composer.list_product_composer import list_product_composer 
from src.errors.error_handler import handle_errors
from src.functions.auth_decorator import login_required

product_route_bp = Blueprint("product_routes", __name__)

@product_route_bp.route("/products", methods=["GET"])
@login_required(role="dono")
def list_products():
    try:
        http_request = HttpRequest()
        view = list_product_composer()
        http_response = view.handle(http_request)
        
        if http_request.headers.get('Accept') == 'application/json':
            return jsonify(http_response.body), http_response.status_code
        else:
            return render_template(
                "product_table.html",
                data=http_response.body["data"]  # Corrigido para "data"
            )
            
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code