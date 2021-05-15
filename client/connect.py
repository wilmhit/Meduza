from .channels import ConnectionManager
from .voip import VoipClient
from threading import Thread
import time

SERVER_ADDRESS = "127.0.0.1"
METADATA_PORT = 50001

thread_variables = {
    "break_condition": True
}

def connect():
    connection = ConnectionManager(SERVER_ADDRESS, METADATA_PORT)
    #connection.check_sever()
    if True: #connection.connect_channel(1): 
        connection.port = 1515
        voip_client = VoipClient(SERVER_ADDRESS, connection.port)
        timeout_thread = Thread(target=change_timeout)
        timeout_thread.start()
        voip_client.loop_while(thread_variables)
        timeout_thread.join()

def change_timeout():
    time.sleep(5)
    thread_variables["break_condition"] = not thread_variables["break_condition"]
    print("condition changed")
