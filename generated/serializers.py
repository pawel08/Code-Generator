from dataclasses import dataclass
import struct
from typing import Tuple


def _pack_string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    return struct.pack("!H", len(encoded)) + encoded


def _unpack_string(data: bytes, offset: int) -> Tuple[str, int]:
    length = struct.unpack_from("!H", data, offset)[0]
    offset += 2
    value = data[offset:offset + length].decode("utf-8")
    return value, offset + length

@dataclass
class SensorData:
    sensor_id: int
    temperature: float
    humidity: float

    def to_bytes(self) -> bytes:
        chunks = []
        chunks.append(struct.pack("!H", self.sensor_id))
        chunks.append(struct.pack("!f", self.temperature))
        chunks.append(struct.pack("!f", self.humidity))
        return b"".join(chunks)

    @classmethod
    def from_bytes(cls, data: bytes) -> "SensorData":
        offset = 0
        sensor_id = struct.unpack_from("!H", data, offset)[0]
        offset += struct.calcsize("!H")
        temperature = struct.unpack_from("!f", data, offset)[0]
        offset += struct.calcsize("!f")
        humidity = struct.unpack_from("!f", data, offset)[0]
        offset += struct.calcsize("!f")
        return cls(sensor_id=sensor_id, temperature=temperature, humidity=humidity)

@dataclass
class Command:
    command_id: int
    value: int
    description: str
    note: str

    def to_bytes(self) -> bytes:
        chunks = []
        chunks.append(struct.pack("!B", self.command_id))
        chunks.append(struct.pack("!i", self.value))
        chunks.append(_pack_string(self.description))
        chunks.append(_pack_string(self.note))
        return b"".join(chunks)

    @classmethod
    def from_bytes(cls, data: bytes) -> "Command":
        offset = 0
        command_id = struct.unpack_from("!B", data, offset)[0]
        offset += struct.calcsize("!B")
        value = struct.unpack_from("!i", data, offset)[0]
        offset += struct.calcsize("!i")
        description, offset = _unpack_string(data, offset)
        note, offset = _unpack_string(data, offset)
        return cls(command_id=command_id, value=value, description=description, note=note)

