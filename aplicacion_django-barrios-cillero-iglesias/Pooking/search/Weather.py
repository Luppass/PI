class Weather:
    
        def __init__(self, lon, lat, icon, temp_actual, ciudad):
                self.lon = lon
                self.lat = lat
                self.icon = icon
                self.temp_actual = temp_actual
                self.ciudad = ciudad
        
        def getLon(self):
                return self.lon
        def getLat(self):
                return self.lat
        def getIcon(self):
                return self.icon
        def getTemp_actual(self):
                return "{:.1f}".format(self.temp_actual - 273)
        def getCiudad(self):
                return self.ciudad