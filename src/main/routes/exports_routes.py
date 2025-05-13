from flask import Blueprint, jsonify, render_template, send_file
from src.main.composer.exports_composer import exports_composer
from src.views.http_types.http_request import HttpRequest
from src.errors.error_handler import handle_errors
from io import BytesIO
from src.functions.auth_decorator import login_required

exports_route_bp = Blueprint("exports_routes", __name__)
views = exports_composer()

@exports_route_bp.route("/export", methods=["GET"])
@login_required(role="dono")
def export_page():
    try:
        return render_template("export.html")
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@exports_route_bp.route("/export/customer", methods=["GET"])
@login_required(role="dono")
def export_customer():
    try:
        http_request = HttpRequest()
        excel_file: BytesIO = views["customer_export_view"].handle_export(http_request)

        return send_file(
            excel_file,
            as_attachment=True,
            download_name="clientes.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@exports_route_bp.route("/export/product", methods=["GET"])
@login_required(role="dono")
def export_product():
    try:
        http_request = HttpRequest()
        excel_file: BytesIO = views["product_export_view"].handle_export(http_request)

        return send_file(
            excel_file,
            as_attachment=True,
            download_name="produtos.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@exports_route_bp.route("/export/historico", methods=["GET"])
@login_required(role="dono")
def export_historico():
    try:
        http_request = HttpRequest()
        excel_file: BytesIO = views["historico_export_view"].handle_export(http_request)

        return send_file(
            excel_file,
            as_attachment=True,
            download_name="historico_de_vendas.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code
