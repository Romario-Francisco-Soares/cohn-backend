from pydantic import BaseModel, field_validator
import re

class ISayHelloDto(BaseModel):
    message: str

class LoginRequestDto(BaseModel):
    nomeEmpresa: str
    login: str
    password: str

class TokenDTO(BaseModel):
    token: str
#
#    @field_validator("token")
#    def validate_jwt_format(cls, value: str) -> str:
#        """
#        Valida se o token segue o formato JWT: header.payload.signature
#        """
#        jwt_pattern = r'^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$'
#        if not re.match(jwt_pattern, value):
#            raise ValueError("Token JWT inválido no formato")
#        return value
