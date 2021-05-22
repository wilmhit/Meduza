from threading import Thread

from .connect import ConnectionManager
from .gui import run_gui
from server_utils.echo import EchoServer
from .gui_callbacks import gui_state


def main():
    connection_manager = ConnectionManager(gui_state)

    ui_thread = Thread(target=run_gui)
    ui_thread.start()
    ui_thread.join()

def mock_main():
    address = ("127.0.0.1", 50002)
    audio_server = EchoServer(address)
    audio_server.start()

    connection_manager = ConnectionManager(gui_state)
    connection_manager.start()

    try:
        connection_manager.wait_for_join()
    except KeyboardInterrupt:
        print("Shutting down...")
        connection_manager.stop()

    audio_server.stop()
