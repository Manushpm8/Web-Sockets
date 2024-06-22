# Manush Murali
# mpmurali@uci.edu
# 14568752


# Class & Module Imports
from WebAPI import WebAPI 
from urllib import request,error
import urllib
import json


# ExtraCreditAPI Class
# The ExtraCreditAPI class creates objects containing information regarding the current title of a business category news using the News WebAPI.
class ExtraCreditAPI(WebAPI):
    
    # Class Constructor/Initializer
    def __init__(self):
        EXTRACREDITAPIKEY = "8ea4935483f14bf5a264c44d923f30bd"
        self.apikey = EXTRACREDITAPIKEY
        self.url = ""
        self.response = ""
    
    # This method sets and loads parts of JSON fromatted data into the class attributes.
    def load_data(self) -> None:
        self.url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={self.apikey}"
        news_obj = super()._download_url(self.url)
        self.response = news_obj['articles'][0]['title']
        
    # This method takes in the post of the user and replaces all the "@extracredit" keyword with the information containing the title of a business category news.
    def transclude(self, message: str) -> str:
        x = message.replace("@extracredit", self.response)
        return x