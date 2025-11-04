from pydantic import BaseModel

class ISayHelloDto(BaseModel):
    message: str

class LoginRequest(BaseModel):
    nomeEmpresa: str
    usuario: str
    senha: str