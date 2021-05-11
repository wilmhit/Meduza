from threading import Thread
from .gui import run_gui
from .connect import connect
from server_utils.echo import EchoServer


def main():
    ui_thread = Thread(target=run_gui)
    #ui_thread.start()
    connect()
    #ui_thread.join()

def mock_main():
    address = ("127.0.0.1", 50002)
    audio_server = EchoServer(address)
    audio_server.start()
    

