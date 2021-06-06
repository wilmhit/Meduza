from threading import Thread
from random import randint
from .connect import ConnectionManager
from .channels import ChannelManager
from .gui import run_gui
from server_utils.dummy_audio import DummyAudioClient
from .gui_callbacks import gui_state

PORT_MIN = 51100
PORT_MAX = PORT_MIN + 500

def main():
    connection_manager = ConnectionManager(gui_state, ("127.0.0.1", 50002))
    connection_manager.start()

    ui_thread = Thread(target=run_gui)
    ui_thread.start()
    ui_thread.join()
    connection_manager.stop()

def mock_main():
    local_address = ("127.0.0.1", randint(PORT_MIN, PORT_MAX))
    server_address = ("127.0.0.1", 50001) # Metadata port

    channel_to_connect = 2

    try:
        channels = ChannelManager(server_address, local_address)

        print("Ping result: ", channels.ping())
        connection_succesful = channels.connect_channel(channel_to_connect)
        print("Connecting result: ", connection_succesful)
        if connection_succesful:
            print("Channel port: ", channels.port)

        channel_address = ("127.0.0.1", channels.port)
        client = DummyAudioClient(local_address,
                                channel_address,
                                soc=channels.metadata_socket)
        client.start()
    except KeyboardInterrupt:
        print("\nShutting down")
        client.stop()
