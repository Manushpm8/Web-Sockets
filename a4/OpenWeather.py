# Manush Murali
# mpmurali@uci.edu
# 14568752


# Class & Module Imports
from WebAPI import WebAPI 
from urllib import request,error
import urllib
import json


# OpenWeather Class
# The OpenWeather class creates objects containing information regarding the current weather description using the OpenWeather WebAPI.
class OpenWeather(WebAPI):
    
    # Class Constructor/Initializer
    def __init__(self, zp = "92697", cc = "US"):
        self.zip = zp
        self.ccode = cc
        self.apikey = ""
        self.url = ""
        self.temperature = ""
        self.high_temperature = ""
        self.low_temperature = ""
        self.longitude = ""
        self.latitude = ""
        self.description = ""
        self.humidity = ""
        self.city = ""
        self.sunset = ""
    
    # This method sets and loads parts of JSON fromatted data into the class attributes.
    def load_data(self) -> None:
        self.url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zip},{self.ccode}&appid={super().get_apikey()}"
        weather_obj = super()._download_url(self.url)
        if weather_obj is not None:
            self.temperature = weather_obj['main']['temp']
            self.high_temperature = weather_obj['main']['temp_min']
            self.low_temperature = weather_obj['main']['temp_max']
            self.longitude = weather_obj['coord']['lon']
            self.latitude = weather_obj['coord']['lat']
            self.description = weather_obj['weather'][0]['description']
            self.humidity = weather_obj['main']['humidity']
            self.city = weather_obj['name']
            self.sunset = weather_obj['sys']['sunset']

    # This method takes in the post of the user and replaces all the "@weather" keyword with the information containing the current weather.
    def transclude(self, message: str) -> str:
        x = message.replace("@weather", self.description)
        return x
            

