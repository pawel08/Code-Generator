import os
import sys
import socket
import threading
from pathlib import Path
from typing import Optional

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from generated.serializers import SensorData, Command

HOST = "127.0.0.1"
PORT = 5000


def handle_client(conn: socket.socket) -> None:
    data = conn.recv(1024)
    if not data:
        return

    try:
        message = SensorData.from_bytes(data)
        print(f"Received SensorData: {message}")
        response = f"OK sensor {message.sensor_id}".encode("utf-8")
    except Exception:
        command = Command.from_bytes(data)
        print(f"Received Command: {command}")
        response = f"Command {command.command_id} value={command.value}".encode("utf-8")

    conn.sendall(response)


def run_server(stop_event: Optional[threading.Event] = None) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(1)
        srv.settimeout(0.5)
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            if stop_event is not None and stop_event.is_set():
                print("Server stop requested")
                break
            try:
                conn, addr = srv.accept()
            except socket.timeout:
                continue
            with conn:
                print(f"Connected by {addr}")
                handle_client(conn)
        print("Server stopped")


if __name__ == "__main__":
    run_server()
