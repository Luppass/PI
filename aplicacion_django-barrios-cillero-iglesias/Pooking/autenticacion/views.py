from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse

def inicioDeSesion(request):
    if request.method == 'POST':
        #en el formulario del login se manda el nombre de usuario y la contraseña
        nombre = request.POST.get('uname')
        contraseña = request.POST.get('psw')
        #se comprueba en el framework de autenticacion de Django si es el usuario y contraseñas correcto
        usuario = authenticate(username=nombre, password=contraseña)
        #si no es valido devuelve None
        if usuario is None:
            return render(request,'errorLogin.html')
        else:
            #si esta es valido el par nombre contraseña, en la request logeamos al usuario para que este en todas las paginas logeado
            login(request,usuario)
            return redirect('index')
            
    return render(request,'login.html')

def noAuth(request):
    return render(request,'noAutenticado.html')

def registro(request):
    if request.method == 'POST':
        if request.POST.get('passwd') != request.POST.get('repitedpasswd'):
           return HttpResponse(status=204)
        try:
            user = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('passwd'))
            user.save()
            login(request,user)
            return redirect('index')
        except IntegrityError:
            context = {'userAlreadyExists' : 'Ya existe un usuario con el nombre \"' + str(request.POST.get('username')) + '\". Escoga otro por favor'}
            return render(request,'registerUserAlreadyExist.html',context)

    return render(request,'register.html')