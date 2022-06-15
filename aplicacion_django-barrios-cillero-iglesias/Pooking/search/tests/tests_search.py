from django.test import TestCase
from django.test import Client
from .. import weatherAPI
from .. import SitesAPI
from datetime import datetime
from datetime import timedelta

class SearchTestCase(TestCase):

    def test_introducirCiudad(self):
        username = "testing"
        passwd = "passwordtesting"
        email = "test@testing.com"
        c = Client()
        response = c.post(
            '/registro', {'username': username,
                'passwd': passwd,
                'repitedpasswd': passwd,
                'email': email})
        self.assertEquals(response.status_code, 302)#te redirije al index por lo que es una redireccion 302
        self.assertTrue(c.login(username=username, password=passwd))

        response = c.post('/search/', {'lugar' : 'coruña', 'radio' : 5})
        self.assertEquals(response.status_code, 200) # POST con éxito
        self.assertTrue(b'The Clock Museum' in response.content)
        self.assertTrue(b'Monument to Maria Pita' in response.content)

    def test_weather(self):
        w = weatherAPI.weatherAPI()
        w.weatherByCity('A Coruña')
        w.dataAsign()
        lat = w.weather.getLat()
        lon = w.weather.getLon()
        self.assertTrue(w.weather.getCiudad() == 'A Coruña')
        #se comprueba que devuelve la misma ciudad
        w.weatherByCoordinates(lat,lon)
        w.dataAsign()
        self.assertTrue(w.weather.getCiudad() == 'A Coruña')
        #con esto miramos que el numero es un float bien formado
        self.assertTrue(type(float(w.weather.getTemp_actual())) is float)
        #la latitud y la longitud no creemos que merezca la pena comprobarlas ya
        #que no sabemos como comprobarla bien para cada ciudad ya que varian con
        #lo que se indica en cada pagina web
        w.weatherByCity('Santiago')
        w.dataAsign()
        lat = w.weather.getLat()
        lon = w.weather.getLon()
        self.assertTrue(w.weather.getCiudad() == 'Santiago')
        w.weatherByCoordinates(lat,lon)
        w.dataAsign()
        self.assertTrue(w.weather.getCiudad() == 'Santiago')
        self.assertTrue(type(float(w.weather.getTemp_actual())) is float)
        w.weatherByCity('Madrid')
        w.dataAsign()
        lat = w.weather.getLat()
        lon = w.weather.getLon()
        self.assertTrue(w.weather.getCiudad() == 'Madrid')
        w.weatherByCoordinates(lat,lon)
        w.dataAsign()
        #en algunos casos la API falla al ubicar la ciudad, no devuelve la
        #ciudad exacta o en algunos casos ubica otra ciudad/distrito distinto.
        #Aunque es cosa de la API, nosotros no podemos hacer nada
        self.assertTrue('Madrid' in w.weather.getCiudad() or 'Sol' in w.weather.getCiudad(),msg=w.weather.getCiudad())
        self.assertTrue(type(float(w.weather.getTemp_actual())) is float)
        #comprobando que devuelve EXIT cuando no es una ciudad valida
        self.assertEqual('EXIT',w.weatherByCity('aaaa'))
        self.assertEqual('EXIT',w.weatherByCity('test'))
        self.assertEqual('EXIT',w.weatherByCity('asdvbafb'))

    def test_time(self):
        #se comprueba que el tiempo esta en el rango adecuado.

        #se le restan dos minutos a before y suman dos a after porque no incluye
        #segundos y es para darle algo de margen
        before = datetime.now() - timedelta(minutes=2)
        w = weatherAPI.weatherAPI()
        w.actualTime()
        enMedio = w.time
        after = datetime.now()
        after = after + timedelta(minutes=2)
        self.assertLess(before,datetime.strptime(enMedio, '%d-%m-%Y %H:%M'))
        self.assertLess(datetime.strptime(enMedio, '%d-%m-%Y %H:%M'),after)

    def test_sites(self):
        s = SitesAPI.SitesAPI()
        #se le ponen las coordenadas de Barcelona
        s.ApiSites(5000,2.159,41.3888)
        s.dataframeWithoutDiscts()
        df = s.getSites()
        self.assertFalse(len(df[df['name'] == 'Tower of Hercules']) > 0)
        self.assertTrue(len(df[df['name'] == 'Rambla de Catalunya']) > 0)
        self.assertTrue(len(df[df['name'] == 'Casa Garriga Nogués']) > 0)
        self.assertTrue(len(df[df['name'] == 'Font del Trinxa']) > 0)
        #se le ponen las coordenadas de Coruña
        s.ApiSites(5000,-8.396,43.3713)
        s.dataframeWithoutDiscts()
        df = s.getSites()
        self.assertTrue(len(df[df['name'] == 'Palacio municipal de La Coruña']) > 0)
        self.assertTrue(len(df[df['name'] == 'Monument to Maria Pita']) > 0)
        self.assertTrue(len(df[df['name'] == 'Teatro Rosalía de Castro']) > 0)
        self.assertTrue(len(df[df['name'] == 'Tower of Hercules']) > 0)
        s.filtroPorKind('churches')
        df = s.getSites()
        self.assertFalse(False in df['kinds'].str.contains('churches').tolist())
        s.filtroPorKind('other_churches')
        df = s.getSites()
        self.assertFalse(False in df['kinds'].str.contains('other_churches').tolist())
        #al ser todos de otras iglesias no existe ninguna que sea catolica
        self.assertTrue(False in df['kinds'].str.contains('catholic_churches').tolist())
        s.ApiSites(5000,-8.396,43.3713)
        s.dataframeWithoutDiscts()
        s.filtroPorKind('churches')
        #ordenacion de menor a mayor
        s.ordenarPor('rate',True)
        df = s.getSites()
        aux = df['rate']
        auxlist = aux.tolist()
        auxlistsort = auxlist.copy()
        auxlistsort.sort()
        for i,x in enumerate(auxlist):
            self.assertTrue(x == auxlistsort[i])
        #ordenacion de mayor a menor
        s.ordenarPor('rate',False)
        df = s.getSites()
        aux = df['rate']
        auxlist = aux.tolist()
        auxlistreverse = auxlist.copy()
        auxlistreverse.sort()
        auxlistreverse.reverse()
        for i,x in enumerate(auxlist):
            self.assertTrue(x == auxlistreverse[i])

