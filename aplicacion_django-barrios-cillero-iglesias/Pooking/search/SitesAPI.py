import requests
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
#en la funcion de SitesAPI llamada createListOfSites hacemos
#df['kinds'] = df['kinds'].apply(lambda x : x.split(',')) 
#lo cual nos da un warning. No nos supone un problema por lo que lo quitamos

class SitesAPI:
        
        def __init__(self):
            self.__apikey="5ae2e3f221c38a28845f05b656fa07d7077f03ed3f5796571cb110e6"
            self.__json = None
            self.sites = None
        #funcion que hace una peticion opentripmap para conseguir ubicaciones alrededor
        #de una ubicacion en un area circular. Se le pasa el tamaño del radio (int) EN METROS, la
        #longitud y la latitud (float)
        #EL RADIO EN METROS OJO
        
        def ApiSites(self,radius, lon, lat):
                endopoint="http://api.opentripmap.com/0.1/en/places/radius?"
                formato="geojson" # format
                enlace = endopoint + "radius=" + str(int(radius)) + "&lon=" + str(float(lon))  +  "&lat=" + str(float(lat)) + "&format=" + formato + "&apikey=" + self.__apikey
                self.__json = requests.get(enlace).json()
        #Transforma el json resultante de ApiSites en uno sin jsons internos 
        
        def dataframeWithoutDiscts(self):
                newJSON = []
                aux = {}
                #lo recorremos ya quitandole la definicion de FeatureCollection
                for x in self.__json.get("features"):
                        aux.update({'type':x.get('type')})
                        aux.update({'id':x.get('id')})
                        aux.update({'geometryType':x.get('geometry').get('type')})
                        aux.update({'geometryCoordinateslon':x.get('geometry').get('coordinates')[0]})
                        aux.update({'geometryCoordinateslat':x.get('geometry').get('coordinates')[1]})
                        aux.update({'name':x.get('properties').get('name')})
                        aux.update({'dist':x.get('properties').get('dist')})
                        aux.update({'rate':x.get('properties').get('rate')})
                        aux.update({'xid':x.get('properties').get('xid')})
                        aux.update({'kinds':x.get('properties').get('kinds')})
                        newJSON.append(aux.copy())
                        aux.clear()
                self.sites = pd.DataFrame.from_dict(newJSON)
        
        def knowSites(self,radius, lon, lat):
                self.ApiSites(radius,lon,lat)
                self.dataframeWithoutDiscts()
        
        def getSites(self):
                return self.sites

        def createListOfSites(self):
                df = self.sites[['name','geometryCoordinateslat','geometryCoordinateslon','rate','kinds','xid']]
                df['kinds'] = df['kinds'].apply(lambda x : x.split(','))
                df = df[df['name'] != '']
                l = df.values.tolist()
                return l
        
        def filtroPorKind(self,kind):
                self.sites = self.sites[self.sites['kinds'].str.contains(kind)]

        def ordenarPor(self,atributo,ascendente):
                self.sites = self.sites.sort_values(by=[atributo], ascending=ascendente)
        
        def infoSitio(self,xid):
                endpoint="http://api.opentripmap.com/0.1/en/places/xid/"
                enlace = endpoint + xid + "?apikey=" + self.__apikey
                respuesta = requests.get(enlace).json()
                informacion = {}
                try:
                        informacion.update({'imagenURL' : respuesta.get('preview').get('source')})
                except:
                        informacion.update({'imagenURL' :''})
                try:
                        #informacion.update({'descripcion' : respuesta.get('wikipedia_extracts').get('text')})
                        informacion.update({'descripcion' : respuesta.get('wikipedia_extracts').get('html')})
                except:
                        informacion.update({'descripcion' : ''})
                informacion.update({'lon' : respuesta.get('point').get('lon')})
                informacion.update({'lat' : respuesta.get('point').get('lat')})

                return informacion








# a = df[['columna1','columna2']] == select de sql
# a.to_json() pasa a json
# a.values.tolist() pasa a una lista de listas