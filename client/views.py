from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        self.connect("destroy", Gtk.main_quit)
        self.set_titlebar(self.Header())
        self.add(self.MainContent())

    class Header(Gtk.HeaderBar):
        def __init__(self):
            Gtk.HeaderBar.__init__(self, title="Headerbar title")
            self.set_show_close_button(True)
    
    class MainContent(Gtk.Grid):
        def __init__(self):
            Gtk.Grid.__init__(self)

            
