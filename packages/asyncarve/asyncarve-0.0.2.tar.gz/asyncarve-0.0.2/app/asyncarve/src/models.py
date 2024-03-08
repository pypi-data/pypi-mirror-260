from __future__ import annotations

from dataclasses import dataclass, field
from mashumaro import field_options
from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin
from mashumaro.types import SerializationStrategy


class IntegerIsBoolean(SerializationStrategy):
    """Boolean serialization strategy for integers."""

    def serialize(self, value: bool) -> int:  # noqa: FBT001
        """Serialize a boolean to an integer."""
        return int(value)

    def deserialize(self, value: int) -> bool:
        """Deserialize an integer to a boolean."""
        return bool(value)


class BaseModel(DataClassORJSONMixin):
    class Config(BaseConfig):

        omit_none = True
        serialization_strategy = {bool: IntegerIsBoolean()}
        serialize_by_alias = True


@dataclass
class ArveSensPro(BaseModel):
    name: str = field(metadata=field_options(alias="name"))
    firmware_vers: str = field(metadata=field_options(alias="firmwareversion"))
    device_vers: str = field(metadata=field_options(alias="deviceversion"))


@dataclass
class ArveSensProData(BaseModel):
    aqi: int
    co2: float
    humidity: float
    pm10: float
    pm25: float
    temperature: float
    tvoc: int

# @dataclass
# class SomeClass:
#     name: str = field(metadata=field_options(alias="name"))
