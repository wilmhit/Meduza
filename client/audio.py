import socket

# This is basic draft
# Make this work for now
# It doesn't need to change channels or talk to gui as of now

def connect():
    connection = ConnectionManager()
    # connection.connect_channel(user_selected_channel)
    # use pyAudio to open recording and listening streams
    # while True:
    # throw recv_audio_packet() to listening stream
    # throw send_audio_packet() to recording stream


class ConnectionManager():

    def __init__():
        # Open 2 random ports: 1. Metadata port 2. Audio port
        # Check here connection to server metadata port using
        # client metadata port
        pass

    def connect_channel(channel):
        ## ESTABLISHING AUDIO PORT
        # Send request from client metadata port to server metadata port
        # In request include channel you want to connect to
        # Server sends back audio port
        ## PUNCHING UDP HOLE
        # Idk how to solve this. Client needs to send packet to first.
        # Why? Server doesn't know what is client's audio port. You can't
        # just send port number. NAT might change it without client knowing
        # about it. Check wikipedia: UDP hole punching.
        pass
    
    def recv_audio_packet():
        # This method reads client audio port buffer
        # Will raise an error if used before connect_channel(channel)
        pass

    def send_audio_packet():
        # Same as above
        pass


