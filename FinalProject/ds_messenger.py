# Manush Murali
# mpmurali@uci.edu
# 14568752

# Shreyas V Chandramouli
# svchand1@uci.edu
# 70688884


# Class Imports
import json
import ds_protocol
import time
import socket
import re



class DirectMessage:
    """ 
    The DirectMessage class is responsible for working with individual user message. It currently supports Three features: 
    A timestamp property that is set upon instantiation and when the entry object is set and an 
    recipient property that stores the recipient name and message propoerty that stores the messages.
    """
    def __init__(self, message:str = None, recipient:str = None, timestamp:float = 0):
        self.timestamp = timestamp
        self.set_message(message)
        self.set_recipient(recipient)
    
    def set_message(self, message):
        self.message = message

        # If timestamp has not been set, generate a new from time module.
        if self.timestamp == 0 or self.timestamp is None:
            self.timestamp = time.time() 
   
    def set_recipient(self, recipient):
        self.recipient = recipient

        # If timestamp has not been set, generate a new from time module
        if self.timestamp == 0:
            self.timestamp = time.time()  

    def get_message(self):
        return self.message  

    def get_recipient(self):
        return self.recipient 
    
    def set_time(self, timestamp:float):
        self.timestamp = timestamp
    
    def get_time(self):
        return self.timestamp



class DirectMessenger:
    """ 
    The DirectMessenger class is responsible for working with sending and receiving messages with the server in order to allow 
    communication between two users. It currently supports Three features: 
    A timestamp property that is set upon instantiation and when the entry object is set and an 
    recipient property that stores the recipient name and message propoerty that stores the messages.
    """
    def __init__(self, dsuserver:str=None, username:str=None, password:str=None):
        self.timestamp = str(time.time())
        self.username = username
        self.password = password
        self.dsuserver = dsuserver
        if self.dsuserver is None:
            self.dsuserver = "168.235.86.101"
        self.message = ""
        self.token = self.GetToken(self.dsuserver, 3021, self.username, self.password)

    def senddata(self,server:str, port:int, username:str, password:str, message:str, bio:str=None) -> str:
        """
        Sends any message to the server and connects with the server if all protocols are followed.
        Returns the message that the server returns after connection.
        """
        #Sends Data to the server in a manner that is in standard Formatting
        PORT = port
        HOST = server
        try:
                with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as echo_client:
                    echo_client.connect((HOST,PORT))
                    send = echo_client.makefile('w')
                    recv = echo_client.makefile('r')
                    stupid = str(message)
                    regemin = re.compile('(?<!\\\\)\'')
                    WithDouble = regemin.sub('\"',stupid )
                    send.write(WithDouble + "\r\n")
                    send.flush()
                    srv_msg = recv.readline()
                return srv_msg
        except Exception as e:
                print("ERROR",e)
        pass

    def send(self, message:str, recipient:str) -> bool:
        """
        Sends a direct message from the user to the recipient using the server. 
        Returns a boolean value that depicts the status whether the message was succussfully sent.
        """   
        # returns true if message successfully sent, false if send failed.
        self.token = self.GetToken(self.dsuserver,3021,self.username,self.password)
        self.message = message
        sendingwithoutjson = ds_protocol.directmessage_command(self.token,self.message,recipient,self.timestamp)
        p = re.compile('(?<!\\\\)\'')
        someString = p.sub('\"', sendingwithoutjson)
        sendingwithjson = json.loads(someString)
        srv_msg = self.senddata(self.dsuserver,3021,self.username,self.password,sendingwithjson)
        DecodedInput = json.loads(srv_msg)
        Bool = DecodedInput['response']['type']
        #print(Bool)
        if Bool == 'ok':
            return True
        else:
            return False
		
    def retrieve_new(self) -> list:
        """
        Retrieve recent new messages from server and returns list of DirectMessage object.
        """
        # returns a list of DirectMessage objects containing all new messages
        result = []
        sendingwithoutjson = ds_protocol.unreadmessages_command(self.token)
        p = re.compile('(?<!\\\\)\'')
        someString = p.sub('\"', sendingwithoutjson)
        sendingwithjson = json.loads(someString)
        srv_msg = self.senddata(self.dsuserver,3021,self.username,self.password,sendingwithjson)
        DecodedInput = json.loads(srv_msg)
        ListofItems = DecodedInput['response']['messages']
        for i in ListofItems:
            directMessageObject = DirectMessage()
            directMessageObject.recipient = i["from"]
            directMessageObject.message =i["message"]
            directMessageObject.timestamp =i["timestamp"]
            result.append(directMessageObject)
        return result
 
    def retrieve_all(self) -> list:
        """
        Retrieve all messages from server and returns list of DirectMessage object.
        """
        # returns a list of DirectMessage objects containing all messages
        result = []
        sendingwithoutjson = ds_protocol.allmessages_command(self.token)
        print(sendingwithoutjson)
        p = re.compile('(?<!\\\\)\'')
        someString = p.sub('\"', sendingwithoutjson)
        sendingwithjson = json.loads(someString)
        srv_msg = self.senddata(self.dsuserver,3021,self.username,self.password,sendingwithjson)
        DecodedInput = json.loads(srv_msg)
        ListofMessages = DecodedInput['response']['messages']
        for i in ListofMessages:
            directMessageObject = DirectMessage()
            directMessageObject.recipient = i["from"]
            directMessageObject.message =i["message"]
            directMessageObject.timestamp =i["timestamp"]
            result.append(directMessageObject)
        return result

    def GetToken(self, server:str, port:int, username:str, password:str):
        """
        Gets the token of the user from the server using the join protocol.
        """
        # Gets the token for a particular username and Password
        #print("Hi World!")
        PORT = port
        HOST = server
        try:
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as echo_client:
                echo_client.connect((HOST,PORT))
                send = echo_client.makefile('w')
                recv = echo_client.makefile('r')
                Listofitems=str({"join": {"username": username,"password": password,"token":""}})
                #print(Listofitems)
                p = re.compile('(?<!\\\\)\'')
                someString = p.sub('\"', Listofitems)
                ToBeSentTuple=json.loads(someString)
                #print(ToBeSentTuple)
                p = re.compile('(?<!\\\\)\'')
                whatever = p.sub('\"', str(ToBeSentTuple))
                send.write(whatever + "\r\n")
                send.flush()
                srv_msg = recv.readline()
                #print (srv_msg)
                decodedmessage=json.loads(srv_msg)
                user_token=decodedmessage['response']['token']
                return user_token
        except Exception as e:
            print("Error as",e)