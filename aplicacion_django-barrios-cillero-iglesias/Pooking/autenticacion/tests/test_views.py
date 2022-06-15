from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

class ViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="test", password="testpass")

    def test_register(self):
        #se crea un usuario para probar el registro, este usuario se usa solo
        #para esto asique no deberia existir en la BD. El setup se encargo de
        #borrarlo
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
        c.logout()
        self.assertTrue(c.login(username=username, password=passwd))
        c.logout()
        #Se prueba con un mismo usuario registrado
        response = c.post(
            '/registro', {'username': username,
                'passwd': passwd,
                'repitedpasswd': passwd,
                'email': email})
        self.assertEquals(response.status_code, 200)
        self.assertTrue(b'Ya existe un usuario con el nombre' in response.content)
        #se prueba con contraseñas distintas
        response = c.post(
            '/registro', {'username': 'b',
                'passwd': passwd,
                'repitedpasswd': 'a',
                'email': email})
        self.assertEquals(response.status_code, 204)
        

    def test_login(self):
        c = Client()
        response = c.post(
            '/', {'username': 'test', 'password': 'testpass'})
        self.assertEquals(response.status_code, 200)
        c.logout()
        #fallo de login
        response = c.post(
            '/', {'username': 'a', 'password': 'a'})
        self.assertEquals(response.status_code, 200)
        self.assertTrue(b'Error' in response.content)
        self.assertTrue(str.encode('El usuario o contraseña introducido no es correcto.') in response.content)
        