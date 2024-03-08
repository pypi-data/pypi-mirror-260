"""Asynchronous Python client for Arve"""
from __future__ import annotations

import asyncio
import socket
import datetime
import time
from dataclasses import dataclass
from typing import (
    Any,
)

import mashumaro.exceptions
from aiohttp.client import ClientError, ClientSession
from aiohttp.hdrs import METH_GET, METH_POST
from yarl import URL

from ..src.exceptions import ArveError, ArveConnectionError, ArveUnathorizedError
from ..src.const import HOST, PORT, HOST_LOCAL, PORT_LOCAL
from ..src.models import ArveSensProData, ArveSensPro


@dataclass
class Arve:
    """Main class for handling connections with Arve devices"""

    api_key: str
    customer_token: str
    device_sn: str
    request_timeout: int = 10
    session: ClientSession | None = None

    _close_session: bool = False
    _acc_token: str | None = None
    _acc_token_expiration: datetime.datetime | None = None

    async def _request(
        self,
        uri: str,
        headers: dict[str, Any],
        method: str = METH_GET,
        data: dict[str, Any] | None = None
    ) -> dict:
        url = URL.build(
            scheme="https",
            host=HOST,
            port=PORT,
            path=""
        ).join(URL(uri))

        headers = headers

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.request(method, url, json=data, headers=headers)
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            msg = "Timeout occured while connecting to Arve Account"
            raise ArveConnectionError(msg) from exception
        except (
            ClientError,
            socket.gaierror
        ) as exception:
            msg = "Error occured while communicating with Arve devices"
            raise ArveConnectionError(msg) from exception

        return await response.json()

    async def get_sensor_info(self):
        headers = {
            "api_key": f"{self.api_key}",
            "customerToken": f"{self.customer_token}",
            "devicesn": f"{self.device_sn}"
        }

        data_raw: dict = await self._request("/homeassistant/device/deviceInfo", headers)
        data = {key: value for key, value in data_raw.items()}

        try:
            res = ArveSensPro.from_json(f"{data}".replace("'", '"'))
            return res
        except mashumaro.exceptions.MissingField as exception:
            msg = data['message']
            raise ArveError(msg) from exception

    async def device_sensor_data(self):
        # try:
        cur_t = int(time.time())

        fr = str((cur_t - 10) // 10) + "0000"
        to = str(cur_t // 10) + "0000"

        headers = {
            "api_key": f"{self.api_key}",
            "customerToken": f"{self.customer_token}",
            "devicesn": f"{self.device_sn}",
            "from": fr,
            "to": to
        }

        data_raw: dict = await self._request("/homeassistant/device/deviceStatus", headers)
        data = {key: value[0] for key, value in data_raw['queryValues'].items()}

        try:
            res = ArveSensProData.from_json(f"{data}".replace("'", '"'))
            return res
        except mashumaro.exceptions.MissingField as exception:
            msg = data['message']
            raise ArveError(msg) from exception

    async def get_curr_co2(self):
        res = await self.device_sensor_data()
        return res.co2

    async def get_curr_aqi(self):
        res = await self.device_sensor_data()
        return res.aqi

    async def get_curr_humidity(self):
        res = await self.device_sensor_data()
        return res.humidity

    async def get_curr_pm10(self):
        res = await self.device_sensor_data()
        return res.pm10

    async def get_curr_pm25(self):
        res = await self.device_sensor_data()
        return res.pm25

    async def get_curr_temperature(self):
        res = await self.device_sensor_data()
        return res.temperature

    async def get_curr_tvoc(self):
        res = await self.device_sensor_data()
        return res.tvoc

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
