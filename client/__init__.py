from threading import Thread

from .connect import ConnectionManager
from .gui import run_gui
from .gui_callbacks import gui_state


def main():
    ui_thread = Thread(target=run_gui)
    ui_thread.start()
    connection_manager = ConnectionManager(gui_state)
    connection_manager.main_loop()
    ui_thread.join()
