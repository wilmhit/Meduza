import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from views import MainWindow
from threading import Thread

if __name__ == "__main__":
    window = MainWindow()
    window.show_all()
    ui_thread = Thread(target=Gtk.main)
    ui_thread.start()
    ui_thread.join()
    