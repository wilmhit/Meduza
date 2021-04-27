
gui_state = {
    "connect_label": "Connect",
    "channels": {
        "Channel 1": {
            "connected": True
        },
        "Channel 2": {
            "connected": False
        }
    }
}

def disconnect_button(button):
    print("Input received!")
    gui_state["connect_label"] = "Disconnect"

def boom_button(button):
    print("Input received!")

def channel_0_button(button):
    print("Input received!")

def mute_all_checkbox(button):
    print("Input received!")

def mute_mic_checkbox(button):
    print("Input received!")

def channel_callback(channel):
    print(channel)

def cancel_password_modal(button):
    print("Input received!")

def connect_with_password(button):
    print("Input received!")

def get_channels():
    return ["Channel 1", "Channel 2"]