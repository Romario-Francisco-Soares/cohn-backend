from httpx import AsyncClient
from src.index import app
import pytest

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_say_hello():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/hello/John")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello John"}

@pytest.mark.asyncio
async def test_hello_message():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/hello", json={"message": "Alice"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Alice"}

@pytest.mark.asyncio
async def test_login():
    data_post = {
        "nomeEmpresa": "COHN TECHNOLOGY INOVA SIMPLES (I.S.)",
        "login": "Erick Viana Santiago Oliveira",
        "password": "123"
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/login", json=data_post)
    assert response.status_code == 200

