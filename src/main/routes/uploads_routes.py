from flask import Blueprint, jsonify, render_template, request
from src.views.http_types.http_request import HttpRequest
from src.main.composer.upload_composer import upload_composer
import logging
from src.functions.auth_decorator import login_required

logger = logging.getLogger(__name__)
upload_route_bp = Blueprint("upload_routes", __name__)

@upload_route_bp.route("/upload", methods=["GET", "POST"])
@login_required(role="dono")
def handle_uploads():
    try:
        controller = upload_composer()
        
        if request.method == "GET":
            http_request = HttpRequest(
                headers=dict(request.headers),
                method="GET",
                query_params=dict(request.args)
            )
            http_response = controller.handle(http_request)
            return render_template("upload.html", data=http_response.body if http_response else {})
            
        elif request.method == "POST":
            if 'files[]' not in request.files:
                return jsonify({
                    "status": "error",
                    "message": "Nenhum arquivo enviado"
                }), 400
                
            http_request = HttpRequest(
                method="POST",
                files={'files': request.files.getlist('files[]')},
                body=request.form.to_dict()
            )
            
            http_response = controller.handle(http_request)
            
            if not http_response:
                logger.error("Resposta do controller é None")
                return jsonify({
                    "status": "error",
                    "message": "Erro interno no processamento"
                }), 500
                
            return jsonify(http_response.body), http_response.status_code
            
    except Exception as e:
        logger.error(f"Erro no endpoint /upload: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Erro interno no servidor",
            "details": str(e)
        }), 500