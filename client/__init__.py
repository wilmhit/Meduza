from threading import Thread
from .channels import connect
from .gui import run_gui


def main():
    ui_thread = Thread(target=run_gui)
    ui_thread.start()
    #connect()
    ui_thread.join()
