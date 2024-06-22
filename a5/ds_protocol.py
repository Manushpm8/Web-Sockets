# Manush Murali
# mpmurali@uci.edu
# 14568752



# Class, Module, & Library Imports
import json
from collections import namedtuple



# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ['response','type','message'])

def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  try:
    json_obj = json.loads(json_msg)
    response = json_obj['response']
    type = json_obj['response']['type']
    message = json_obj['response']['message']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(response, type, message)


# Join Command JSON Formator
def join_command(username, password, public_key):
    j = "{\"join\": {\"username\": \"" + username + "\",\"password\": \"" + password + "\", \"token\": \"" + public_key + "\"}}"
    return j
# Post Command JSON Formator
def post_command(token, post, timestamp):
    j = "{\"token\":\"" + token + "\", \"post\": {\"entry\": \"" + post + "\", \"timestamp\": \"" + timestamp + "\"}}"
    return j
# Bio Command JSON Formator
def bio_command(token, bio, timestamp):
    j = "{\"token\":\"" + token + "\", \"bio\": {\"entry\": \"" + bio + "\", \"timestamp\": \"" + timestamp + "\"}}"
    return j

