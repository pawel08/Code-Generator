import threading
import time
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from examples.server import run_server
from examples.client import send_sensor_data, send_command


def main() -> None:
    print("[Stage 1] Uruchamianie serwera TCP...")
    stop_event = threading.Event()
    server_thread = threading.Thread(target=run_server, args=(stop_event,), daemon=True)
    server_thread.start()

    time.sleep(1)
    print("[Stage 2] Serwer jest gotowy. Wysyłam pierwszy komunikat typu SensorData...")
    send_sensor_data()

    print("[Stage 3] Wysyłam drugi komunikat typu Command...")
    send_command()

    print("[Stage 4] Zamykanie serwera i kończenie demo...")
    stop_event.set()
    server_thread.join(timeout=2)
    print("[Stage 5] Demo zakończone pomyślnie.")


if __name__ == "__main__":
    main()
