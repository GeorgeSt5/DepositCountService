import asyncio
from typing import AsyncGenerator
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from main import app


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as ac:
        yield ac


# тестовые данные лучше выделить в отдельный файл и парсить из него
@pytest.mark.asyncio
async def test_correct_request(ac: AsyncClient):
    # рабочий запрос
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as ac:
        response = await ac.post("api/deposit_service/calculate_deposit", json={
                                                     "date": "31.01.2021",
                                                     "periods": 3,
                                                     "amount": 10000,
                                                     "rate": 6
                                                     })

        assert response.status_code == 200
        assert response.json() == {
      "31.01.2021": 10050,
      "28.02.2021": 10100.25,
      "31.03.2021": 10150.75
    }


fails = ({"date": "31.01.2021",
          "periods": 3,
          "amount": 10000,
          "rate": 0},
         {"date": "31.01.21",
          "periods": 3,
          "amount": 10000,
          "rate": 5},
         {"date": "31.01.2021",
          "periods": 3,
          "amount": 1,
          "rate": 6},
         {"date": "31.01.2021",
          "periods": -3,
          "amount": 100000,
          "rate": 6},
         {"date": "31.00.000",
          "periods": 0,
          "amount": -1,
          "rate": -3})

@pytest.mark.asyncio
async def test_incorrect_requests(ac: AsyncClient):
    # ощибки валидации
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as ac:
        for fail in fails:
            response = await ac.post("api/deposit_service/calculate_deposit", json=fail)

            assert response.status_code == 400
