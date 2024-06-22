# Manush Murali
# mpmurali@uci.edu
# 14568752

# Shreyas V Chandramouli
# svchand1@uci.edu
# 70688884



# Class Imports
import json
from collections import namedtuple


DataTuple = namedtuple('DataTuple', ['response','type','message'])

def extract_json(json_msg:str) -> DataTuple:
  """
  Call the json.loads function on a json string and convert it to a DataTuple object
  """
  try:
    json_obj = json.loads(json_msg)
    response = json_obj['response']
    type = json_obj['response']['type']
    message = json_obj['response']['message']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(response, type, message)


# Server Joiner
# Join Command JSON Formator
def join_command(username, password):
    """Formats the parameters into the style that is required for the join function"""
    j = "{\"join\": {\"username\": \"" + str(username) + "\", \"password\": \"" + str(password) + "\", \"token\":\"\"}}"
    return j

# Message Receiver
# Send a Direct Message Command JSON Formator
def directmessage_command(user_token, message, recipient, timestamp):
    """Formats the parameters into the style that is required for the direct message function"""
    j = "{\"token\": \"" + str(user_token) + "\", \"directmessage\": {\"entry\": \"" + str(message) + "\", \"recipient\": \"" + str(recipient) + "\", \"timestamp\": \"" + str(timestamp) + "\"}}"
    return j
# Request Unread Messages Command JSON Formator
def unreadmessages_command(user_token):
    """Formats the parameters into the style that is required for the unread function"""
    j = "{\"token\":\"" + str(user_token) + "\", \"directmessage\": \"new\"}"
    return j
# Request All Messages Command JSON Formator
def allmessages_command(user_token):
    """Formats the parameters into the style that is required for the retrieve all msgs function"""
    j = "{\"token\":\"" + str(user_token) + "\", \"directmessage\": \"all\"}"
    return j

