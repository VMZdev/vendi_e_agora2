from flask import Blueprint, render_template, session, redirect, url_for
from src.functions.auth_decorator import login_required

home_route_bp = Blueprint("home_routes", __name__)

@home_route_bp.route("/")
@login_required(role="dono")
def home():
    return render_template("home.html")
