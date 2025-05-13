from src.models.sqlite.entitites.user import UserTable
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

class UserRepository:
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def create_user(self, username: str, password: str) -> bool:
        hashed_password = generate_password_hash(password)
        with self.__db_connection as database:
            existing = database.session.query(UserTable).filter_by(username=username).first()
            if existing:
                return False
            new_user = UserTable(username=username, password=hashed_password)
            database.session.add(new_user)
            database.session.commit()
            return True

    def authenticate_user(self, username: str, password: str) -> UserTable | None:
        with self.__db_connection as database:
            try:
                user = database.session.query(UserTable).filter_by(username=username).first()
                if user and check_password_hash(user.password, password):
                    return user
            except NoResultFound:
                return None