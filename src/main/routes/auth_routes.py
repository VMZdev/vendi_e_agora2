from flask import Blueprint, render_template, request, redirect, url_for, session
from src.views.http_types.http_request import HttpRequest
from src.main.composer.auth_composer import auth_composer

auth_route_bp = Blueprint("auth_routes", __name__)

@auth_route_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        http_request = HttpRequest(body=dict(request.form))
        view = auth_composer()
        response = view.login(http_request)
        if response.status_code == 302:
            return redirect(response.body)
        return render_template("login.html", error=response.body)
    return render_template("login.html", success=request.args.get("success"))

@auth_route_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print("📥 Dados recebidos no formulário:", request.form)
        http_request = HttpRequest(body=dict(request.form))
        view = auth_composer()
        response = view.register(http_request)
        if response.status_code == 302:
            return redirect(response.body)
        return render_template("register.html", error=response.body)
    return render_template("register.html")

@auth_route_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth_routes.login"))
