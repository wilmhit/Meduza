import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from views import MainWindow


if __name__ == "__main__":
    window = MainWindow()
    window.show_all()
    Gtk.main()
