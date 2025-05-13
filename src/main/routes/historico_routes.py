from flask import Blueprint, jsonify, render_template
from src.views.http_types.http_request import HttpRequest
from src.main.composer.list_historico_composer import list_historico_composer 
from src.errors.error_handler import handle_errors
from src.functions.auth_decorator import login_required

historico_route_bp = Blueprint("historico_routes", __name__)

@historico_route_bp.route("/historico", methods=["GET"])
@login_required(role="dono")
def list_historico():
    try:
        http_request = HttpRequest()
        view = list_historico_composer()
        http_response = view.handle(http_request)
        
        # Retorna HTML ou JSON conforme o Accept header
        if http_request.headers.get('Accept') == 'application/json':
            return jsonify(http_response.body), http_response.status_code
        else:
            return render_template(
                "historico_table.html",
                historico=http_response.body
            )
            
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code