from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = os.getenv("DATABASE_URL")
        self.__engine = None
        self.session = None
        self.__session_maker = None
    
    def connect_to_db(self):
        self.__engine = create_engine(self.__connection_string)
        self.__session_maker = sessionmaker(bind=self.__engine)

    def get_engine(self):
        return self.__engine
    
    def get_new_session(self):
        """Returns a new independent session"""
        if not self.__session_maker:
            self.connect_to_db()
        return self.__session_maker()
    
    def __enter__(self):
        if not self.__session_maker:
            self.connect_to_db()
        self.session = self.__session_maker()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()

db_connection_handler = DBConnectionHandler()