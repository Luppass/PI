import requests
from . import Weather 
import pendulum

class weatherAPI:

        def __init__(self):
                self.__api_key = '09a3ae582855d62e4ddc75da42eaee0c'
                self.__data = None
                self.weather = None
                self.time = None

        def getData(self):
                return self.__data

        def __getResponse(self,url):
                response = requests.get(url)
                if response.status_code == 404:
                        return 'EXIT' #error por no encontrar ciudad
                else:
                        self.__data = response.json()

        def weatherByCity(self,city):
                url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + self.__api_key
                return self.__getResponse(url)
        
        def weatherByCoordinates(self,lat,lon):
                url = 'https://api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(lon) + '&appid=' + self.__api_key
                return self.__getResponse(url)
                

        def dataAsign(self):
                self.weather = Weather.Weather(self.__data.get('coord').get('lon'), 
                        self.__data.get('coord').get('lat'),
                        self.__data.get('weather')[0].get('icon'),
                        self.__data.get('main').get('temp'),
                        self.__data.get('name'))
                        
            
        def actualTime(self): # NOTA: se restringe esta utilidad a únicamente España (Península)
                self.time = pendulum.now('Europe/Madrid')
                self.time = self.time.format('DD-MM-YYYY HH:mm')