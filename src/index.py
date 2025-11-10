from src.cached.upstash import get_dados_redis
from src.utils.normalize import normalize_bson
from src.dtos.ISayHelloDto import ISayHelloDto, LoginRequestDto, TokenDTO
from src.data.dataquery.mmongodb import ds_busca_mongo
from src.security.security_headers import create_app
from src.security.authentication import authentify
from src.security.jwt_handler import create_access_token, get_current_data

from fastapi import Depends

app = create_app()

@app.get("/")
async def root():
    regis = await get_dados_redis('6908f8af6c8794e55e3e8536', 'clientes')
    return {"message": normalize_bson(regis)}

@app.post("/login")
async def login(dto: LoginRequestDto):
    item = await ds_busca_mongo("nomeEmpresa", dto.nomeEmpresa, 'clientes')
    if item:
        if authentify(dto.login, dto.password, item.get('profissionais')):
            token = create_access_token({"profissional": dto.login,
                                         "empresa": dto.nomeEmpresa,
                                         "produtos": item.get('produtos')})

            return {"access_token": token, "token_type": "bearer"}
        return {"erro": "Usuário ou senha incorretos"}
    return {"erro": "Empresa não encontrada"}

@app.post("/products_list")
async def products_list(data=Depends(get_current_data)):
    products = [await get_dados_redis(normalize_bson(prod), 'produtos') for prod in data.get('produtos')]
    return products

@app.get("/hello/{name}")
async def say_hello(name: str, data=Depends(get_current_data)):
    return {"message": f"Hello {name}", "data": data}

@app.post("/hello")
async def hello_message(dto: ISayHelloDto, data=Depends(get_current_data)):
    return {"message": f"Hello {dto.message}", "data": data}
