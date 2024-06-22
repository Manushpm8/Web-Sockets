# Manush Murali
# mpmurali@uci.edu
# 14568752

# Shreyas V Chandramouli
# svchand1@uci.edu
# 70688884

# Profile.py
#
# ICS 32 Fall 2021
# Assignment #2: Journal
#
# Author: Mark S. Baldwin
#
# v0.1.7

# You should review this code to identify what features you need to support
# in your program for assignment 2.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THE JSON SERIALIZATION ASPECTS OF THIS CODE RIGHT NOW, 
# though can you certainly take a look at it if you are curious.


# Class Imports
import json, time, os
from pathlib import Path
from tkinter import Message
from typing import List
from ds_messenger import *


class DsuFileError(Exception):
    """
    DsuFileError is a custom exception handler that you should catch in your own code. It
    is raised when attempting to load or save Profile objects to file the system.
    """
    pass


class DsuProfileError(Exception):
    """
    DsuProfileError is a custom exception handler that you should catch in your own code. It
    is raised when attempting to deserialize a dsu file to a Profile object.
    """
    pass


class MessagesException(Exception):
    pass


class Post(dict):
    """ 
    The Post class is responsible for working with individual user posts. It currently supports two features: 
    A timestamp property that is set upon instantiation and when the entry object is set and an 
    entry property that stores the post message. In this case, it also stores messages with all the required details. 
    """
    def __init__(self, message:str = None, recipient:str = None, timestamp:float = 0):
        self._timestamp = timestamp
        self.set_message(message)
        self.set_recipient(recipient)


        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, message = self._message, recipient = self._recipient, timestamp = self._timestamp)
    
    def set_message(self, message):
        """ Gets the entry in the post"""
        self._message = message 
        dict.__setitem__(self, 'message', message)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_message(self):
        """ Sets the entry in the post"""
        return self._message
    
    def set_recipient(self, recipient):
        """ Sets the title of the post stored in the dict"""
        self._recipient = recipient
        dict.__setitem__(self, 'recipient', recipient)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_recipient(self):
        """ Gets the title of the post stored in the dict"""
        return self._recipient
    
    def set_time(self, time:float):
        """ Sets the time for the posts"""
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self):
        """Gets the time of the porsts"""
        return self._timestamp

    """
    The property method is used to support get and set capability for entry and time values.
    When the value for entry is changed, or set, the timestamp field is updated to the
    current time.
    """ 
    message = property(get_message, set_message)
    recipient = property(get_recipient, set_recipient)
    timestamp = property(get_time, set_time)

    
    
class Profile:
    """
    The Profile class creates various recipients for the user to communicate with.
    """
    def __init__(self, username=None, password=None):
        self.username = username         
        self._messages = []
    
    def set_username(self, username):
        """Sets the username of a profile class object."""
        self.username = username

    def get_username(self):
        """Gets the username of a profile class object."""
        return self.username
    
    def add_messages(self,messages: list)->None:
        """Adds a new aspect of the profile class called messages"""
        for message in messages:
            self._messages.append(message)

    def add_message(self, message:str):
        """Adds a message"""
        self._messages.append(message)

    def del_message(self,index:int)->bool:
        """Deletes a Message stored in the profile based on the index"""
        try:
            del self._messages[index]
            return True
        except IndexError:
            return False
    def clear_messages(self)-> None:
        """Clears all the messages in the profile"""
        self._messages = []
        
    def get_messages(self)-> list:
        """ gets all the messages stored in there"""
        return self._messages

    def add_post(self, post: Post) -> None:
        """
        Adds a post to the profile class object.
        """
        self._posts.append(post)
    
    def get_post(self):
        """
        Gets a post from the profile class object.
        """
        return self._posts


    def del_post(self, index: int) -> bool:
        """
        del_post removes a Post (message, recipient, and timestamp) at a given index and returns True if successful and False if an invalid
        index was supplied. 
        """
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False
        
    def get_posts(self) -> list:
        """
        get_posts returns the list object containing all posts (messages, recipients, and timestamps) that have been added to the Profile object.
        """
        return self._posts

    """
    save_profile accepts an existing dsu file to save the current instance of Profile to the file system.
    Example usage:
    profile = Profile()
    profile.save_profile('/path/to/file.dsu')
    Raises DsuFileError
    """
    def save_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("An error occurred while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    """
    load_profile will populate the current instance of Profile with data stored in a DSU file.
    Example usage: 
    profile = Profile()
    profile.load_profile('/path/to/file.dsu')
    Raises DsuProfileError, DsuFileError
    """
    def load_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                for message_obj in obj['_messages']:
                    sent_messages = []
                    received_messages = []
                    if (message_obj['sent_messages'] != None):
                        for sent_msg in message_obj["sent_messages"]:
                            sentmessage = Post(sent_msg['message'], sent_msg['recipient'], sent_msg['timestamp'])
                            sent_messages.append(sentmessage)
                    if message_obj["received_messages"] != None:
                        for received_msg in message_obj["received_messages"]:
                            receivedmessage = Post(received_msg['message'], received_msg['recipient'], received_msg['timestamp'])
                            received_messages.append(receivedmessage)
                    messages =  Messages(message_obj['otheruser'], sent_messages, received_messages)  
                    self._messages.append(messages) 
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()



class Messages(dict):
    '''
    This class stores the messages locally.
    '''
    def __init__(self, otheruser:str, sent_messages:list=None, received_messages:list=None):
        self.otheruser = otheruser
        self.sent_messages = sent_messages
        self.received_messages = received_messages
        dict.__init__(self,otheruser=self.otheruser, sent_messages=self.sent_messages, received_messages=self.received_messages)

    def add_sent_msg(self, message):
        '''
        Adds the directmessage objects to the sent_messages class attribute.
        '''
        self.sent_messages.append(message)
    
    def add_receieved_msg(self, message):
        '''
        Adds the directmessage objects to the received_messages class attribute.
        '''
        self.received_messages.append(message)