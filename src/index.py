from fastapi import FastAPI
from src.dbconect.upstash import get_dados_redis
from src.utils.normalizadorJson import normalize_bson
from src.dtos.ISayHelloDto import ISayHelloDto, LoginRequest
from src.dbconect.mmongodb import nome_empresa_busca_mongo
from src.utils.crypt import descriptografar

app = FastAPI()

def autenticar(usuario, senha, profissionais):
    return any(prof['nome'] == usuario and descriptografar(prof['senha']) == senha for prof in profissionais)

@app.get("/")
async def root():
    regis = await normalize_bson(get_dados_redis('6908f8af6c8794e55e3e8536'))
    return {"message": regis}

@app.post("/login")
async def login(dto: LoginRequest):
    item = await nome_empresa_busca_mongo(dto.nomeEmpresa)
    if item:
        acessar = autenticar(dto.usuario, dto.senha, item.get('profissionais'))
        return {"message": acessar}
    else:
        return {'erro': False}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/hello")
async def hello_message(dto: ISayHelloDto):
    return {"message": f"Hello {dto.message}"}
