from typing import Dict, Optional
from werkzeug.datastructures import FileStorage

class HttpRequest:
    def __init__(
        self,
        headers: Optional[Dict] = None,
        body: Optional[Dict] = None,
        query_params: Optional[Dict] = None,
        files: Optional[Dict[str, FileStorage]] = None,
        method: Optional[str] = None,
        form: Optional[Dict] = None
    ):
        self.headers = headers or {}
        self.body = body or {}
        self.query_params = query_params or {}
        self.files = files or {}
        self.method = method
        self.form = form or {}