"""
Here is all information controlled by gui interface. `gui_state` is a dict
that can be imported in other parts of this software. Additional helper 
functions are below. They should not be imported (should be used only by GUI).
"""
import time
from typing import Dict, Union

S_BETWEEN_CLICKS = 0.005
CHANNELS = 5

gui_state = {
    "is_running": True,
    "mute_mic": False,
    "mute_spk": False,
    "last_click": 0.0,
    "connection_validated": False,
    "password": "",
    "server_ip": "",
    # channel_connected is unnecessary (in theory), since one can get this
    # information by iteration through channels, but reading bool is faster
    # and this value is read very often
    "channel_connected": False, 
    "channels": []
}


# Creating channels

def create_channel(id: int) -> Dict[str, Union[str, bool]]:
    return {"display": "Channel " + str(id), "connected": False}


for x in range(CHANNELS):
    gui_state["channels"].append(create_channel(x))


# Gui callbacks

def destroy():
    gui_state["is_running"] = False
    disconnect()


def is_channel_connected(channel_id: int):
    return gui_state["channels"][channel_id]["connected"]


def is_connected_to_any_channel() -> bool:
    for channel in gui_state["channels"]:
        if channel["connected"]:
            return True
    return False


def is_connected() -> bool:
    return gui_state["connection_validated"]


def disconnect():
    gui_state["connection_validated"] = False
    gui_state["server_ip"] = ""
    gui_state["channel_connected"] = False
    for channel in gui_state["channels"]:
        channel["connected"] = False


def disconnect_channel():
    for channel in gui_state["channels"]:
        channel["connected"] = False
    gui_state["channel_connected"] = False


def time_lock() -> bool:
    current_time = time.thread_time()
    last_time = gui_state["last_click"]
    time_passed = current_time - last_time
    gui_state["last_click"] = current_time
    # difference is negative for first click
    return time_passed > S_BETWEEN_CLICKS or time_passed < 0


def connect_channel(channel_id: int):
    for channel in gui_state["channels"]:
        channel["connected"] = False
    gui_state["channels"][channel_id]["connected"] = True
    gui_state["channel_connected"] = True


def connect_with_password(channel_id: int, password: str):
    gui_state["password"] = password
    connect_channel(channel_id)


def is_protected_channel(channel_id: int):
    return channel_id == 0


def boom_callback(_):
    print("boom") # TODO


def mute_mic(_):
    gui_state["mute_mic"] = not gui_state["mute_mic"]


def connect_to_server(address: str):
    gui_state["server_ip"] = address
    # `gui_state["connected"]` will be changed by `ConnectionManager`
    # when connection is validated


def mute_spk(_):
    gui_state["mute_spk"] = not gui_state["mute_spk"]
