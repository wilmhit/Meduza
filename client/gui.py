import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .views import MainWindow, PasswordModal


def run_gui():
    window = MainWindow()
    window.show_all()
    Gtk.main()
