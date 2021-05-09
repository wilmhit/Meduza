from threading import Thread

from .connect import ConnectionManager
from .gui import run_gui
from .gui_callbacks import gui_state


def main():
    connection_manager = ConnectionManager(gui_state)

    ui_thread = Thread(target=run_gui)
    connection_thread = Thread(target=connection_manager.main_loop)

    ui_thread.start()
    connection_thread.start()

    ui_thread.join()
    connection_thread.join()
