from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Usuarios, Proyectos, miembros_proyecto
from django.contrib.auth.decorators import login_required

import re

# Create your views here.
def inicio(request):
    
    if request.method == 'POST':
        
        
        if not request.user.is_authenticated:
            return render(request, 'inicio.html')
        
        datos = request.POST
        
        if re.fullmatch('^\s+|^\s*$', datos['NombreProyecto']):
            return render(request, 'inicio.html', {
                'aviso': 'No se puede crear con solamente espacios'
            })
        
        if re.fullmatch('^[a-zA-Z0-9\s]{3,}$', datos['NombreProyecto']):
            
            try:
                proyecto = Proyectos(nombre=datos['NombreProyecto'])
                
                creador = miembros_proyecto(id_proyecto=proyecto, usuario=request.user, is_admin=True)

            except:
                return render(request, 'inicio.html', {
                    'aviso': 'Hubo un problema con el servidor'
                })
            
            proyecto.save()
            creador.save()
            
            print(f'Creando Proyecto: {datos["NombreProyecto"]}')
            
        else:
            return render(request, 'inicio.html', {
                'aviso': 'Solamente letras, numeros y espacio'
            })
        
    if request.user.is_authenticated:
        
        userProyectos = miembros_proyecto.objects.filter(usuario=request.user)
        
        
        return render(request, 'inicio.html', {
            'proyectos': userProyectos
        })
    else:
        return render(request, 'inicio.html')

# Se encarga Victor
def Login (request):
    
    if request.user.is_authenticated:
        
        return redirect('Inicio')
    
    if request.method == "POST":
        
        datos = request.POST
        
        userAuth = authenticate(request, username=datos['correo'], password=datos['contraseña'])
        
        if userAuth is not None:
            
            login(request, userAuth)
            return redirect('Inicio')
        
        else:
            
            return render(request, "login.html", {'aviso': True})
    
    return render(request, "login.html")

# Se encarga Victor
def Registro (request):
    
    if request.user.is_authenticated:
        
        return redirect('Inicio')
    
    if request.method == 'POST':
        datos = request.POST
        
        correo = datos['correo']
        nombres = datos['nombres']
        apellidos = datos['apellidos']
        contraseña = datos['contraseña']
        
        Usuarios.objects.create_user(correo=correo, nombre=nombres, apellido=apellidos, password=contraseña)
    
    return render(request, 'registro.html')

@login_required
def CerrarSesion (request):
    logout(request)
    return redirect('Inicio')

# Se Encarga Luis
@login_required
def TableroProyecto (request):
    
    return render(request, 'proyecto/tableros.html')

@login_required
def TableroEstadistica (request):
    
    return render(request, 'proyecto/Estadisticas.html')

@login_required
def Perfil(request):
    
    return render(request, 'perfil.html')

@login_required
def PanelAdmin(request):
    return render(request, 'admin.html')

# Se encarga Miguel
@login_required
def ProyectosAdmin(request):
    
    return render(request, 'admin/ProyectosAdmin.html')

@login_required
def UsuariosAdmin(request):
    return render(request, 'admin/UsuariosAdmin.html')