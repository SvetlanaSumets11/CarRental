from functools import cached_property, lru_cache

from httpx import AsyncClient, AsyncHTTPTransport

from app.core.config import get_settings
from app.core.enums import CarStatuses
from app.internal_gateway.exception_handler import InternalGatewayErrorHandler


class CarGateway:
    PATH_CARS = '/batch-cars'
    PATH_CARS_STATUS = '/update-cars-status'
    RETRIES = 3

    @cached_property
    def __http_client(self) -> AsyncClient:
        return AsyncClient(transport=AsyncHTTPTransport(retries=self.RETRIES))

    @lru_cache
    def __request_url(self, path: str) -> str:
        base_url = get_settings().INTERNAL_CARS_URL.rstrip('/')
        return f'{base_url}{path}'

    @InternalGatewayErrorHandler()
    async def get_cars_by_ids(self, car_ids: list[int]) -> dict:
        response = await self.__http_client.get(
            url=self.__request_url(self.PATH_CARS),
            params={'car_ids': car_ids},
        )
        response.raise_for_status()
        return response.json()

    @InternalGatewayErrorHandler()
    async def update_cars_status(self, car_ids: list[int], status: CarStatuses) -> dict:
        response = await self.__http_client.post(
            url=self.__request_url(self.PATH_CARS_STATUS),
            json={'car_ids': car_ids, 'status': status},
        )
        response.raise_for_status()
        return response.json()
