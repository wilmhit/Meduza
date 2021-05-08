from threading import Thread
from .gui import run_gui
from .connect import connect


def main():
    ui_thread = Thread(target=run_gui)
    #ui_thread.start()
    connect()
    #ui_thread.join()
