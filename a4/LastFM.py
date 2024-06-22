# Manush Murali
# mpmurali@uci.edu
# 14568752


# Class & Module Imports
from WebAPI import WebAPI 
from urllib import request,error
import urllib
import json


# LastFM Class
# The LastFM class creates objects containing information regarding the top tracks of Drake using the LastFM WebAPI.
class LastFM(WebAPI):
    
    # Class Constructor/Initializer
    def __init__(self):
        self.artist = ""
        self.apikey = ""
        self.url = ""
        self.response = ""
    
    # This method sets and loads parts of JSON fromatted data into the class attributes.
    def load_data(self):
        self.artist = "Drake"
        self.url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={self.artist}&api_key={super().get_apikey()}&format=json"
        music_obj = super()._download_url(self.url)
        l = len(music_obj['toptracks']['track'])
        for i in range(0, l-1):
            if (i != l-2):
                self.response = self.response + music_obj['toptracks']['track'][i]['name'] + ", "
            else:
                self.response = self.response + music_obj['toptracks']['track'][i]['name']

    # This method takes in the post of the user and replaces all the "@lastfm" keyword with the information containing the top tracks of Drake.
    def transclude(self, message: str) -> str:
        x = message.replace("@lastfm", self.response)
        return x

        


