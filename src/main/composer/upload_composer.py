from src.models.sqlite.settings.connection import DBConnectionHandler
from src.models.sqlite.repositories.uploads_repository import UploadsRepository
from src.controller.upload_controller import UploadController

def upload_composer():
    # Initialize dependencies in correct order
    db_connection = DBConnectionHandler()  # First create connection
    repository = UploadsRepository(db_connection)  # Then pass to repository
    controller = UploadController(repository)  # Then pass to controller
    return controller