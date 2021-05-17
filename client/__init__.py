from threading import Thread

from .connect import ConnectionManager
from .gui import run_gui
from .connect import connect
from server_utils.echo import EchoServer
from .gui_callbacks import gui_state


def main():
    connection_manager = ConnectionManager(gui_state)

    ui_thread = Thread(target=run_gui)
    #ui_thread.start()
    connect()
    #ui_thread.join()

def mock_main():
    address = ("127.0.0.1", 50002)
    audio_server = EchoServer(address)
    audio_server.start()
    

    connection_thread = Thread(target=connection_manager.main_loop)

    ui_thread.start()
    connection_thread.start()

    ui_thread.join()
    connection_thread.join()
