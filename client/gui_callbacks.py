import time

S_BETWEEN_CLICKS = 0.005
CHANNELS = 5

gui_state = {
    "muted_mic": False,
    "muted_spk": False,
    "last_click": 0.0,
    "connected": False,
    "channels": []
}

def create_channel(id):
    return {
        "display": "Channel " + str(id),
        "connected": False
    }

for x in range(CHANNELS):
    gui_state["channels"].append(create_channel(x))


def is_channel_connected(channel_id):
    return gui_state["channels"][channel_id]["connected"]

def is_connected_to_any_channel():
    for channel in gui_state["channels"]:
        if channel["connected"]:
            return True
    return False

def is_connected():
    return gui_state["connected"] 

def disconnect():
    gui_state["connected"] = False
    for channel in gui_state["channels"]:
        channel["connected"] = False

def time_lock():
    current_time = time.thread_time()
    last_time = gui_state["last_click"]
    time_passed = current_time - last_time
    gui_state["last_click"] = current_time
    # is negative for first click
    return time_passed > S_BETWEEN_CLICKS or time_passed < 0

def connect_channel(channel_id):
    for channel in gui_state["channels"]:
        channel["connected"] = False
    gui_state["channels"][channel_id]["connected"] = True

def connect_with_password(channel_id, password): 
    connect_channel(channel_id)

def is_protected_channel(channel_id):
    return channel_id == 0

def boom_callback():
    print("boom")

def mute_mic(_):
    pass

def connect_to_server(address):
    gui_state["connected"] = True

def mute_spk(_):
    pass