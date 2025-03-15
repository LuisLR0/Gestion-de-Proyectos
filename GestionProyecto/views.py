from django.shortcuts import render

# Create your views here.
def inicio(request):
    
    return render(request, 'inicio.html')

# Se encarga Victor
def Login (request):
    
    return render(request, "login.html")

# Se encarga Victor
def Registro (request):
    
    return render(request, 'registro.html')

# Se Encarga Luis
def TableroProyecto (request):
    
    return render(request, 'proyecto/tableros.html')

def TableroEstadistica (request):
    
    return render(request, 'proyecto/Estadisticas.html')

def Perfil(request):
    
    return render(request, 'perfil.html')

def PanelAdmin(request):
    return render(request, 'admin.html')

# Se encarga Miguel
def ProyectosAdmin(request):
    
    return render(request, 'admin/ProyectosAdmin.html')

def UsuariosAdmin(request):
    return render(request, 'admin/UsuariosAdmin.html')