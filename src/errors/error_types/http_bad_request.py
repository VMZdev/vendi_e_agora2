class HttpBadRequestError(Exception): # Classe de erro

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.status_code = 400
        self.name = "BadRequest"
        self.message = message