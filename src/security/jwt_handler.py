import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configurações
SECRET_KEY = 'HIOswl8K_CxxofMJ8WhTvgrUK6yePIFqnPXzxVohDUc='
# Ideal: SECRET_KEY = os.getenv("SECRET_KEY", "chave_super_secreta_cohn")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Middleware HTTP Bearer (usado nas rotas protegidas)
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Cria uma Ficha JWT assinado contendo as informações do usuário.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """
    Descodifica e valida o token JWT.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

def get_current_data_bearer(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """ Valida o token de header Authorization.
        Exemplo de uso: `user = Depends(get_current_data)`"""
    return verify_token(credentials.credentials)

def get_current_data_cookie(cookie: str):
    """ Valida o token de cookie
        Exemplo de uso: `user = Depends(get_current_data_cookie(cookie))`"""
    return verify_token(cookie) if cookie else None
