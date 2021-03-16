from gi.repository import Gtk
import gui_callbacks

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.connect("destroy", Gtk.main_quit)
        #self.set_default_size(700, 500)
        self.set_border_width(20)
        self.set_titlebar(Header())
        self.add(MainContent())

class Header(Gtk.HeaderBar):
    def __init__(self):
        Gtk.HeaderBar.__init__(self, title="Meduza 007")
        self.set_show_close_button(True)

        disconnect_button = Gtk.Button(label="Disconnect")
        disconnect_button.connect("clicked", gui_callbacks.disconnect_button)
        self.pack_start(disconnect_button)

class MainContent(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_column_spacing(10)
        self.set_row_spacing(10)

        boom_button = Gtk.Button(label="Detonate")
        channel_0_button = Gtk.Button(label="Connenct to channel 0")
        mute_mic_checkbox = Gtk.CheckButton(label="Mute mic")
        mute_all_checkbox = Gtk.CheckButton(label="Mute all")

        channel_list = Gtk.ListBox()
        framed_channel_list = Gtk.Frame()
        framed_channel_list.add(channel_list)

        boom_button.connect("clicked", gui_callbacks.boom_button)
        channel_0_button.connect("clicked", gui_callbacks.channel_0_button)
        mute_mic_checkbox.connect("clicked", gui_callbacks.mute_mic_checkbox)
        mute_all_checkbox.connect("clicked", gui_callbacks.mute_all_checkbox)

        for channel in self.get_channels():
            channel_list.add(channel)

        self.attach(framed_channel_list, 0, 0, 1, 4)
        self.attach(mute_all_checkbox,   1, 0, 1, 1)
        self.attach(mute_mic_checkbox,   1, 1, 1, 1)
        self.attach(boom_button,         1, 2, 1, 1)
        self.attach(channel_0_button,    1, 3, 1, 1)

    def get_channels(self):
        channels: list = gui_callbacks.get_channels()
        return [self.map_channel(c) for c in channels]

    def map_channel(self, c):
        row = Gtk.ListBoxRow()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(Gtk.Label(label=c), True, True, 0)
        box.pack_start(Gtk.RadioButton(label="connected?"), True, True,0)
        box.connect("clicked", gui_callbacks.)
        row.add(box)
        return row
