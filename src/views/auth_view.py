from flask import session
from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse
from src.controller.auth_controller import AuthController

class AuthView:
    def __init__(self, controller: AuthController):
        self.__controller = controller

    def login(self, http_request: HttpRequest) -> HttpResponse:
        data = http_request.body
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return HttpResponse(status_code=400, body="Usuário e senha são obrigatórios.")

        user = self.__controller.login(username, password)
        if user:
            if user.role != 'dono':
                return HttpResponse(status_code=403, body="Acesso não autorizado.")
            session['user_id'] = user.user_id
            session['role'] = user.role
            return HttpResponse(status_code=302, body="/")
        return HttpResponse(status_code=401, body="Credenciais inválidas")

    def register(self, http_request: HttpRequest) -> HttpResponse:
        data = http_request.body
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return HttpResponse(status_code=400, body="Usuário e senha são obrigatórios.")

        success = self.__controller.register(username, password)
        if success:
            return HttpResponse(status_code=302, body="/login?success=1")
        return HttpResponse(status_code=400, body="Usuário já existe")
