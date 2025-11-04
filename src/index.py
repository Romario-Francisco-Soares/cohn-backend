from fastapi import FastAPI
from src.dbconect.upstash import get_dados_redis
from src.dtos.ISayHelloDto import ISayHelloDto

app = FastAPI()

@app.get("/")
async def root():
    regis = await get_dados_redis('6908f8af6c8794e55e3e8536')
    return {"message": regis}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/hello")
async def hello_message(dto: ISayHelloDto):
    return {"message": f"Hello {dto.message}"}
