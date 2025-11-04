import pytest

from src.dtos.ISayHelloDto import ISayHelloDto, LoginRequest
from src.index import root, say_hello, hello_message, login


@pytest.mark.asyncio
async def test_root():
    result = await root()
    assert result['message']['nomeEmpresa'] == 'COHN TECHNOLOGY INOVA SIMPLES (I.S.)'


@pytest.mark.asyncio
async def test_login():
    data_post = {
        'nomeEmpresa':'COHN TECHNOLOGY INOVA SIMPLES (I.S.)',
        'usuario':'Erick Viana Santiago Oliveira',
        'senha':'123'
    }
    dto = LoginRequest(**data_post)
    result = await login(dto)
    assert result == {'message': True}


@pytest.mark.asyncio
async def test_say_hello():
    result = await say_hello("John")
    assert result == {'message': 'Hello John'}


@pytest.mark.asyncio
async def test_hello_message():
    dto = ISayHelloDto(message="Alice")
    result = await hello_message(dto)
    assert result == {'message': 'Hello Alice'}
