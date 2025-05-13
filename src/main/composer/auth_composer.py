from src.models.sqlite.settings.connection import db_connection_handler
from src.models.sqlite.repositories.user_repository import UserRepository
from src.controller.auth_controller import AuthController
from src.views.auth_view import AuthView

def auth_composer():
    repo = UserRepository(db_connection_handler)
    controller = AuthController(repo)
    view = AuthView(controller)
    return view