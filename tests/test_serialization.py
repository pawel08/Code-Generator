import pytest
from generated.serializers import SensorData, Command


def test_sensor_data_roundtrip() -> None:
    original = SensorData(sensor_id=1000, temperature=18.75, humidity=33.5)
    data = original.to_bytes()
    decoded = SensorData.from_bytes(data)

    assert decoded == original


def test_command_roundtrip() -> None:
    original = Command(command_id=10, value=-42, description="Hello", note="demo")
    data = original.to_bytes()
    decoded = Command.from_bytes(data)

    assert decoded == original
