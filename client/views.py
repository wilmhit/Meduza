from gi.repository import Gtk
from . import gui_callbacks

MAX_PASSWORD_LEN = 10

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self):
        Gtk.ApplicationWindow.__init__(self)
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(20)
        self.set_titlebar(MainHeaderBar(self.show_dialog))
        self.add(MainContent())

    def show_dialog(self, _):
        PasswordModal(self).run()

class MainHeaderBar(Gtk.HeaderBar):
    def __init__(self, disconnect_callback):
        Gtk.HeaderBar.__init__(self, title="Meduza 007")
        self.set_show_close_button(True)

        disconnect_button = Gtk.Button(label="Disconnect")
        disconnect_button.connect("clicked", disconnect_callback)
        self.pack_start(disconnect_button)

class MainContent(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_column_spacing(10)
        self.set_row_spacing(10)

        boom_button = Gtk.Button(label="Detonate")
        mute_mic_checkbox = Gtk.CheckButton(label="Mute mic")
        mute_all_checkbox = Gtk.CheckButton(label="Mute all")

        channel_list = Gtk.ListBox()
        framed_channel_list = Gtk.Frame()
        framed_channel_list.add(channel_list)

        boom_button.connect("clicked", gui_callbacks.boom_button)
        mute_mic_checkbox.connect("clicked", gui_callbacks.mute_mic_checkbox)
        mute_all_checkbox.connect("clicked", gui_callbacks.mute_all_checkbox)

        for channel in self.get_channels():
            channel_list.add(channel)

        # Row Column Width Height        R  C  W  H
        self.attach(framed_channel_list, 0, 0, 1, 4)
        self.attach(mute_all_checkbox,   1, 0, 1, 1)
        self.attach(mute_mic_checkbox,   1, 1, 1, 1)
        self.attach(boom_button,         1, 2, 1, 1)
        self.attach(channel_0_button,    1, 3, 1, 1)

    def get_channels(self):
        channels: list = gui_callbacks.get_channels()
        return [self.map_channel(c) for c in channels]

    def map_channel(self, channel):
        row = Gtk.ListBoxRow()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.set_border_width(5)

        radio = Gtk.RadioButton(label=channel)
        radio.connect("clicked", lambda _ : gui_callbacks.channel_callback(c))

        box.pack_start(radio, True, True, 0)
        row.add(box)
        return row

class PasswordModal(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, parent=parent, use_header_bar=True)
        self.add_button("_OK", Gtk.ResponseType.OK)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.connect("response", self.on_response)

        label = Gtk.Label("Password is needed to connect to this channel")
        label.set_padding(30, 30)
        label.set_justify(Gtk.Justification.CENTER)

        self.entry = Gtk.Entry()
        self.entry.set_max_length(MAX_PASSWORD_LEN)
        self.entry.set_margin_bottom(30)
        self.entry.set_margin_left(30)
        self.entry.set_margin_right(30)

        self.vbox.add(label)
        self.vbox.add(self.entry)
        self.vbox.set_border_width(10)
        self.show_all()

    def on_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            print(self.entry.get_text())
        else:
            print("Cancel button clicked")
        dialog.destroy()
