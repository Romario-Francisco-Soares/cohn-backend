from httpx import AsyncClient
from src.index import app
import pytest

_headers = {}

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

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_products_list():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/products_list")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_say_hello_authenticated():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/hello", json={"message": "John"})

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello John"
    assert "data" in data
    assert data["data"]["profissional"] == "Erick Viana Santiago Oliveira"

@pytest.mark.asyncio
async def test_hello_message():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/hello", json={"message": "Alice"})
    assert response.status_code == 200
