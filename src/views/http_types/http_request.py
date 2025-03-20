from typing import Dict

class HttpRequest:
    def __init__(self, body: Dict = None, param: Dict = None) -> None: # Dict = None -> Caso meu body não seja preenchido por nada, ele me retorna um None
        self.body = body
        self.param = param
