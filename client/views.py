from gi.repository import Gtk, GLib

from . import gui_callbacks
from .gui_callbacks import gui_state

MAX_PASSWORD_LEN = 10
MAX_SERVER_ADDRESS = 1000

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self):
        Gtk.ApplicationWindow.__init__(self)
        self.connect("destroy", self.destroy)
        self.set_border_width(20)
        self.set_titlebar(MainHeaderBar(self))
        self.add(MainContent(self))

    def destroy(self, *args, **kwargs):
        gui_callbacks.destroy()
        Gtk.main_quit(*args, **kwargs)

    def show_dialog(self, _):
        PasswordModal(self).run()

class MainHeaderBar(Gtk.HeaderBar):
    def __init__(self, parent):
        self.parent = parent
        Gtk.HeaderBar.__init__(self, title="Meduza 007")
        self.set_show_close_button(True)

        self.disconnect_button = Gtk.Button(label=self.get_connect_label())
        self.disconnect_button.connect("clicked", self.connect)
        self.pack_start(self.disconnect_button)
        self.timeout_id = GLib.timeout_add(500, self.on_timeout, None)

    def get_connect_label(self):
        if gui_callbacks.is_connected():
            return "Disconnect"
        return "Connect"

    def connect(self, button):
        if not gui_callbacks.is_connected():
            ServerModal(self.parent).run()
        else:
            gui_callbacks.disconnect()
        button.set_label(self.get_connect_label())

    def on_timeout(self, _):
        if self.get_connect_label() != self.disconnect_button.get_label():
            self.disconnect_button.set_label(self.get_connect_label())
        return True

class MainContent(Gtk.Grid):
    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.set_column_spacing(10)
        self.set_row_spacing(10)
        self.parent = parent
        self.channels = self.create_channel_list()

        boom_button = Gtk.Button(label="Detonate")
        mute_mic_checkbox = Gtk.CheckButton(label="Mute mic")
        mute_all_checkbox = Gtk.CheckButton(label="Mute all")

        boom_button.set_margin_left(50)
        mute_all_checkbox.set_margin_left(50)
        mute_mic_checkbox.set_margin_left(50)
        boom_button.set_margin_right(50)
        mute_all_checkbox.set_margin_right(50)
        mute_mic_checkbox.set_margin_right(50)

        channel_list = Gtk.ListBox()
        framed_channel_list = Gtk.Frame()
        framed_channel_list.add(channel_list)

        boom_button.connect("clicked", gui_callbacks.boom_callback)
        mute_mic_checkbox.connect("clicked", gui_callbacks.mute_mic)
        mute_all_checkbox.connect("clicked", gui_callbacks.mute_spk)

        for channel in self.channels:
            channel_list.add(channel[0])

        gui_state["update_gui"] = self.set_connected_channels

        # Row Column Width Height        R  C  W  H
        self.attach(framed_channel_list, 0, 0, 1, 4)
        self.attach(mute_all_checkbox,   1, 0, 1, 1)
        self.attach(mute_mic_checkbox,   1, 1, 1, 1)
        self.attach(boom_button,         1, 2, 1, 1)

    def create_channel_list(self):
        return [
            self.map_channel(c, c_id)
            for c_id, c in enumerate(gui_state["channels"])
        ]

    def set_connected_channels(self):
        for channel_id, channel in enumerate(self.channels):
            state = gui_callbacks.is_channel_connected(channel_id)
            self.set_channel_active(channel, state)
    
    def set_channel_active(self, channel, state):
        checkbox = channel[1]
        if checkbox.get_active() != state:
            checkbox.set_active(state)

    def map_channel(self, channel, channel_id):
        row = Gtk.ListBoxRow()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.set_border_width(5)
        box.set_margin_left(30)
        box.set_margin_right(30)
        checkbox = Gtk.CheckButton(label=channel["display"])

        def checkbox_callback(channel_id):
            self.channel_click(channel_id)
            self.set_connected_channels()

        checkbox.connect("clicked", lambda _: checkbox_callback(channel_id))

        box.pack_start(checkbox, True, True, 0)
        row.add(box)
        return row, checkbox
    
    def channel_click(self, channel_id):
        if not gui_callbacks.time_lock() or not gui_callbacks.is_connected():
            return
        if gui_callbacks.is_channel_connected(channel_id):
            return gui_callbacks.disconnect_channel()

        if gui_callbacks.is_protected_channel(channel_id):
            PasswordModal(self.parent).run()
        else:
            gui_callbacks.connect_channel(channel_id)


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
            gui_callbacks.connect_with_password(0, self.entry.get_text())
            gui_callbacks.time_lock()
        else:
            gui_callbacks.time_lock()
        dialog.destroy()

class ServerModal(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, parent=parent, use_header_bar=True)
        self.add_button("_OK", Gtk.ResponseType.OK)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.connect("response", self.on_response)

        label = Gtk.Label("Please enter server address")
        label.set_padding(30, 30)
        label.set_justify(Gtk.Justification.CENTER)

        self.entry = Gtk.Entry()
        self.entry.set_max_length(MAX_SERVER_ADDRESS)
        self.entry.set_margin_bottom(30)
        self.entry.set_margin_left(30)
        self.entry.set_margin_right(30)

        self.vbox.add(label)
        self.vbox.add(self.entry)
        self.vbox.set_border_width(10)
        self.show_all()

    def on_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            gui_callbacks.connect_to_server(self.entry.get_text())
        dialog.destroy()
