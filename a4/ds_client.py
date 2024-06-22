# Manush Murali
# mpmurali@uci.edu
# 14568752


# Class Imports
import socket
import json
import time
import Profile
import ds_protocol

# Communicator Function
# This function sends the messages and/or bio inputed by the user to a user-inputed Distributed Social Server.
def communicator(server:str, port:int, username:str, password:str, message:str, bio:str=None):
    '''
    The send function joins a ds server and sends a message, bio, or both
    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.p
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try: 
            client.connect((server, port))
            send = client.makefile('w')
            recv = client.makefile('r')
            send.write(message + "\r\n")
            send.flush()
            js_msg = recv.readline()
            return js_msg
        except Exception as e:
            print(e)
    pass


# Send Function
# This function communicates with the Distributed Social Server directly and adds/edits posts/bios based on the User-Inputed Profiles.
def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
    '''
    The send function joins a ds server and sends a message, bio, or both
    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''

    try:
        js = "{\"join\": {\"username\": \"" + username + "\",\"password\": \"" + password + "\",\"token\":\"\"}}"
        js_msg = communicator(server, port, username, password, js)
        ds_msg = json.loads(js_msg)
        tok = ds_msg["response"]["token"]
        po = Profile.Post(entry = message, timestamp = time.time())
        ts = str(po.get_time())
        js = ds_protocol.post_command(tok, message, ts)
        final_msg = communicator(server, port, username, password, js)
        print(ds_protocol.extract_json(final_msg).message)
    except Exception as e:
            print(e)
    pass