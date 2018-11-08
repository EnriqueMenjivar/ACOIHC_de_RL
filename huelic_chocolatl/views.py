from django.http import HttpResponse 
from django.shortcuts import render
import datetime

def prueba_logout(request): 
    ahora = datetime.datetime.now() 
    html = "<html><body><h1>Fecha:</h1><h3>%s<h/3><h1>Funciona :)</h1></body></html>" %ahora 
    return HttpResponse(html)

def home(request):
	return render(request, 'index.html')

	