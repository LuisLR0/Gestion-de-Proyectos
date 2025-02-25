from django.shortcuts import render

# Create your views here.
def inicio(request):
    
    return render(request, 'index.html')

def Login (request):
    
    return render(request, "login.html")

def Registro (request):
    
    return render(request, 'registro.html')

def Proyectos (request):
    
    return render(request, 'proyectos.html')