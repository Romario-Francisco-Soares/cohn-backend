from src.cached.upstash import get_dados_redis
from src.utils.normalize import normalize_bson
from src.dtos.ISayHelloDto import ISayHelloDto, LoginRequest
from src.data.dataquery.mmongodb import nome_empresa_busca_mongo
from src.security.security_headers import create_app
from src.security.authentication import authentify

app = create_app()

@app.get("/")
async def root():
    regis = await get_dados_redis('6908f8af6c8794e55e3e8536')
    return {"message": normalize_bson(regis)}

@app.post("/login")
async def login(dto: LoginRequest):
    item = await nome_empresa_busca_mongo(dto.nomeEmpresa)
    if item:
        return {"message": authentify(dto.login, dto.password, item.get('profissionais'))
}
    else:
        return {'erro': False}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/hello")
async def hello_message(dto: ISayHelloDto):
    return {"message": f"Hello {dto.message}"}
