from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI


class ClientParametreRequestException(HTTPException):    
    def __init__(self, msg: str, status_code: int, params: dict):
        # Adiciona o atributo 'params' antes de chamar o construtor da classe base
        self.params = params
        super().__init__(status_code, msg)  # 'detail' agora é passado corretamente
        
    def __str__(self):
        return f"Erro: {self.detail}"   
    

    
class Xlr8HttpExceptionFastAPI(HTTPException):
    pass


