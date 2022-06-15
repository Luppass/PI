from django.shortcuts import redirect, render
from django.http import HttpResponse
import json
from . import weatherAPI
from . import SitesAPI

def __ciudadNoEncontrada(request):
    return render(request,'error.html')

def __ordenacionDelDataframe(request,s):
    ma = request.POST.get('mayor-menor')
    me = request.POST.get('menor-mayor')
    if ma is not None or me is not None:
        if ma and me:
            s.ordenarPor('rate',False)
        elif ma:
            s.ordenarPor('rate',False)
        elif me:
            s.ordenarPor('rate',True)

def index(request):
    #request es <class 'django.core.handlers.wsgi.WSGIRequest'>
    if not request.user.is_authenticated:
        return redirect('Inicie Sesión')

    if request.method == 'POST':
        return map(request)
            
            
    return render(request,'index.html')

def map(request):
    if not request.user.is_authenticated:
        return redirect('Inicie Sesión')

    if request.method == 'POST':
        w = weatherAPI.weatherAPI()
        s = SitesAPI.SitesAPI()
        if len(request.POST.dict()) == 0 and request.body != None:
            data = json.loads(request.body.decode('utf8'))
            if w.weatherByCoordinates(data.get('lat'),data.get('lon')) == 'EXIT':
                return __ciudadNoEncontrada(request)
            w.dataAsign()
            w.actualTime()
            s.knowSites((str(data.get('radio'))+'000'),data.get('lon'),data.get('lat'))
            context = {'listaDeLocalizaciones' : s.createListOfSites(),'lon': str(data.get('lon')), 
                    'lat': str(data.get('lat')), 'ciudad': w.weather.getCiudad, 'temp': w.weather.getTemp_actual,
                    'icon': w.weather.getIcon, 'time': w.time,'radio':data.get('radio')}
            return render(request,'map.html',context)

        if request.POST.get('lugar') != None:
            if w.weatherByCity(request.POST.get('lugar')) == 'EXIT':
                return __ciudadNoEncontrada(request)
            w.dataAsign()
            w.actualTime() 
            if request.POST.get('lat') is not None and request.POST.get('lon') is not None:
                lat = request.POST.get('lat')
                lon = request.POST.get('lon')
            else:
                lat = w.weather.getLat()
                lon = w.weather.getLon()
            #con los getters de w.weather se consigue todo
            #se le pone *1000 al radio porque tiene que pasarsele en metros a la web de la aplicacion
            s.knowSites((request.POST.get('radio')+'000'),lon,lat)
            #se esta aplicando un filtro desde maps
            if request.POST.get('tipolugar') != None:
                s.filtroPorKind(request.POST.get('tipolugar'))
            __ordenacionDelDataframe(request,s)

            context = {'listaDeLocalizaciones' : s.createListOfSites(),'lon': str(lon), 
                    'lat': str(lat), 'ciudad': w.weather.getCiudad, 'temp': w.weather.getTemp_actual,
                    'icon': w.weather.getIcon, 'time': w.time,'radio':request.POST.get('radio')}
            return render(request,'map.html',context) 
    
        else:
            return render(request,'error.html') #No es un post de ninguna de las anteriores
    
    else:
        return redirect('index')
    
def site(request,xid):
    if not request.user.is_authenticated:
        return redirect('Inicie Sesión')

    s = SitesAPI.SitesAPI()
    data = s.infoSitio(xid)
    return HttpResponse(json.dumps(data), content_type = "application/json")
    