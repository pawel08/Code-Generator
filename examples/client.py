import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import socket
from generated.serializers import SensorData, Command

HOST = "127.0.0.1"
PORT = 5000


def send_sensor_data() -> None:
    packet = SensorData(sensor_id=42, temperature=21.5, humidity=56.2).to_bytes()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(packet)
        response = sock.recv(1024)
        print("Server response:", response.decode("utf-8"))


def send_command() -> None:
    packet = Command(command_id=1, value=-123, description="Test command", note="demo").to_bytes()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(packet)
        response = sock.recv(1024)
        print("Server response:", response.decode("utf-8"))


if __name__ == "__main__":
    send_sensor_data()
    send_command()
