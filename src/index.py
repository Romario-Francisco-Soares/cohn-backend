from src.cached.upstash import get_dados_redis
from src.utils.normalize import normalize_bson
from src.dtos.ISayHelloDto import ISayHelloDto, LoginRequestDto, SystemIdAcess
from src.data.dataquery.mmongodb import ds_busca_mongo
from src.security.security import create_app, setting_cookies
from src.security.authentication import authentify
from src.security.jwt_handler import create_access_token, get_current_data_cookie, get_current_data_bearer

from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import Depends, Request

app = create_app()

@app.get("/")
async def root():
    regis = await get_dados_redis('6908f8af6c8794e55e3e8536', 'clientes')
    return {"message": normalize_bson(regis)}

@app.post("/login")
async def login(dto: LoginRequestDto):
    partner_data = await ds_busca_mongo("nomeEmpresa", dto.nomeEmpresa, 'clientes')

    if not partner_data:
        return {"erro": "Dados de acesso incorretos"}

    if not authentify(dto.login, dto.password, partner_data.get('profissionais')):
        return {"erro": "Dados de acesso incorretos"}

    token = create_access_token(
        {"profissional": dto.login,
         "empresa": dto.nomeEmpresa,
         "produtos": partner_data.get('produtos')
         }
    )
    response_json = JSONResponse({"message": "Login efetuado com sucesso"})
    response = setting_cookies(response_json, token, "access_token")
    return response

@app.get("/products_list")
async def products_list(request: Request):
    cookie = request.cookies.get("access_token")
    if not cookie:
        return {"erro": "Erro de cookies"}

    data = get_current_data_cookie(cookie=cookie)
    if not data:
        return {"erro": "Erro de dados"}

    products = [await get_dados_redis(normalize_bson(prod), 'produtos') for prod in data.get('produtos')]
    if not products:
        return {"erro": "Erro de produtos"}

    response_json = JSONResponse(products)
    response = setting_cookies(response_json, cookie, "access_token")
    return response

@app.post("/product_access")
async def product_access(request: Request, dto: SystemIdAcess):
    cookie = request.cookies.get("access_token")
    if not cookie:
        return {"erro": "Erro de cookies"}

    products = await get_dados_redis(normalize_bson(dto.systemId), 'produtos')
    if not products:
        return {"erro": "Erro de produtos"}

    url = products.get("url_sistema")
    if not url:
        return {"erro": "Erro em url de sistemas"}

    redirect_response = RedirectResponse(url=url, status_code=302)

    response = setting_cookies(redirect_response, cookie, "access_token")

    return response

@app.get("/hello/{name}")
async def say_hello(name: str, data=Depends(get_current_data_bearer)):
    return {"message": f"Hello {name}", "data": data}

@app.post("/hello")
async def hello_message(dto: ISayHelloDto, data=Depends(get_current_data_bearer)):
    return {"message": f"Hello {dto.message}", "data": data}
