import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from .views import MainWindow, PasswordModal

def run_gui():
    window = MainWindow()
    #modal = PasswordModal()
    window.show_all()
    #modal.show_all()
    Gtk.main()
