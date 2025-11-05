from pydantic import BaseModel

class ISayHelloDto(BaseModel):
    message: str

class LoginRequest(BaseModel):
    nomeEmpresa: str
    login: str
    password: str