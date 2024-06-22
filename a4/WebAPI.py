# Manush Murali
# mpmurali@uci.edu
# 14568752


# Class & Module Imports
from abc import ABC, abstractmethod
from urllib import request,error
import urllib
import json


# WebAPI class
# # The WebAPI class creates objects of a class that other WebAPIs inherit from.
class WebAPI(ABC):
    
    # Class Constructor/Initializer
    def __init__(self):
        self.apikey = ""
    
    # This method returns the data requested from a WebAPI in the form of a dictionary.
    def _download_url(self, url: str) -> dict:
        #TODO: Implement WebAPI request code in a way that supports all types of WebAPIs.
        response = None
        r_obj = None
        try:
            response = urllib.request.urlopen(url)
            json_results = response.read()
            r_obj = json.loads(json_results)

        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL')
            print('Status Code: {}'.format(e.code))
            if (e.code == 400):
                print("ERROR - Bad Request")
            elif (e.code == 401):
                print("ERROR - User Unauthorized")
            elif (e.code == 403):
                print("ERROR - User Forbidden")
            elif (e.code == 404):
                print("ERROR - Server Not Found")
            elif (e.code == 500):
                print("ERROR - Internal Server Error")
            elif (e.code == 504):
                print("ERROR - Gateway Timeout")

        finally:
            if response != None:
                response.close()
        
        return r_obj
	
    # This method sets the API key of an object from a class connected to a respective WebAPI.
    def set_apikey(self, apikey:str) -> None:
        self.apikey = apikey

    # This method gets the API key of the respective WebAPI.
    def get_apikey(self):
        return self.apikey
	
    # This method sets and loads parts of JSON fromatted data into the class attributes.
    @abstractmethod
    def load_data(self):
        pass
	
    # This method takes in the post of the user and replaces all the keywords with the information contained in the respective WebAPIs.
    @abstractmethod
    def transclude(self, message:str) -> str:
        pass
