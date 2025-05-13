from flask import Blueprint, jsonify, render_template, request
from src.views.http_types.http_request import HttpRequest
from src.main.composer.list_customer_composer import list_customer_composer 
from src.errors.error_handler import handle_errors
from src.functions.auth_decorator import login_required

customer_route_bp = Blueprint("customer_routes", __name__)

@customer_route_bp.route("/customers", methods=["GET"])
@login_required(role="dono")
def list_customers():
    try:
        http_request = HttpRequest(headers=dict(request.headers))
        view = list_customer_composer()
        http_response = view.handle(http_request)
        
        # Adicione esta condição para retornar HTML ou JSON
        if http_request.headers.get('Accept') == 'application/json':
            return jsonify(http_response.body), http_response.status_code
        else:
            return render_template(
                "customers_table.html",
                customers=http_response.body
            )
            
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code