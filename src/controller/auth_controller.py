from src.models.sqlite.repositories.user_repository import UserRepository

class AuthController:
    def __init__(self, user_repository: UserRepository):
        self.__repo = user_repository

    def register(self, username: str, password: str) -> bool:
        return self.__repo.create_user(username, password)

    def login(self, username: str, password: str):
        return self.__repo.authenticate_user(username, password)
