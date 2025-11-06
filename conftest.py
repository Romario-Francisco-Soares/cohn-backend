
import asyncio
import pytest

@pytest.fixture(scope="session")
def event_loop():
    """Cria um único loop de evento compartilhado entre todos os testes assíncronos."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()