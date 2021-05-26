from threading import Thread

from .connect import ConnectionManager
from .channels import ChannelManager
from .gui import run_gui
from server_utils.dummy_audio import DummyAudioClient
from .gui_callbacks import gui_state


def main():
    connection_manager = ConnectionManager(gui_state, ("127.0.0.1", 50002))

    ui_thread = Thread(target=run_gui)
    ui_thread.start()
    ui_thread.join()

def mock_main():
    local_address = ("127.0.0.1", 50002)
    server_address = ("127.0.0.1", 50001) # Metadata port

    channel_to_connect = 2

    try:
        channels = ChannelManager(server_address, local_address)
        channel_address = ("127.0.0.1", channels.port)
        client = DummyAudioClient(local_address,
                                  channel_address,
                                  soc=channels.metadata_socket)

        print("Ping result: ", channels.ping())
        connection_succesful = channels.connect_channel(channel_to_connect)
        print("Connecting result: ", connection_succesful)
        if connection_succesful:
            print("Channel port: ", channels.port)

        client.start()
    except KeyboardInterrupt:
        print("\nShutting down")
        client.stop()
