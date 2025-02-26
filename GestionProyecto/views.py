from django.shortcuts import render

# Create your views here.
def inicio(request):
    
    return render(request, 'inicio.html')

def Login (request):
    
    return render(request, "login.html")

def Registro (request):
    
    return render(request, 'registro.html')

def TableroProyecto (request):
    
    return render(request, 'proyecto/tableros.html')

def TableroEstadistica (request):
    
    return render(request, 'proyecto/Estadisticas.html')