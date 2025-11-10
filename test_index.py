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
        global _headers
        _headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_products_list():
    global _headers
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/products_list", headers=_headers)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_say_hello_authenticated():
    global _headers
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/hello", json={"message": "John"}, headers=_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello John"
    assert "data" in data
    assert data["data"]["profissional"] == "Erick Viana Santiago Oliveira"

@pytest.mark.asyncio
async def test_hello_message():
    global _headers
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/hello", json={"message": "Alice"}, headers=_headers)
    assert response.status_code == 200
