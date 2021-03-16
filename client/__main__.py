import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from views import MainWindow
import socket
import logging
import threading
import time


if __name__ == "__main__":
    window = MainWindow()
    window.show_all()
    Gtk.main() # do osobnego threda
