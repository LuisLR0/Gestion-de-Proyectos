from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Usuarios, Proyectos, miembros_proyecto, tareas_proyecto, tareas as TareasDB, categorias, categorias_proyecto

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

            except Exception as Err:
                print(Err)
                return render(request, 'inicio.html', {
                    'aviso': 'Hubo un problema con el servidor'
                })
            
            proyecto.save()
            creador.save()
            
            for idCategoria in range(1,5):
                
                categoriaPredeterminada = categorias.objects.get(pk=idCategoria)
                
                CategoriaProyecto = categorias_proyecto(id_proyecto=proyecto, id_categoria=categoriaPredeterminada)
                
                CategoriaProyecto.save()
            
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


def CerrarSesion (request):
    
    # Para que no entre a esta ruta si no esta logeado
    if not request.user.is_authenticated:
        
        return redirect('Inicio')
    
    logout(request)
    return redirect('Inicio')

# Se Encarga Luis

def TableroProyecto (request, id_proyecto):
    
    # Para que no entre a esta ruta si no esta logeado
    if not request.user.is_authenticated:
        
        return redirect('Inicio')
    
    miembros = miembros_proyecto.objects.filter(id_proyecto=id_proyecto)
    CategoriasProyecto = categorias_proyecto.objects.filter(id_proyecto=id_proyecto)
    tareas = tareas_proyecto.objects.filter(id_proyecto=id_proyecto)
    proyectoDB = Proyectos.objects.get(pk=id_proyecto)
    miembroAdmin = miembros_proyecto.objects.get(id_proyecto=id_proyecto, usuario=request.user)

    
    if request.method == "POST":
        
        tipoPost = request.POST.get('tipoPost')
        
        datos = request.POST
        
        if tipoPost == "CrearTarea":
            
            print(datos)

            if not re.fullmatch("^[a-zA-Z0-9\s]{1,}$", datos['DescripcionTarea']):
                return render(request, 'proyecto/tableros.html', {
                    "id_proyecto": id_proyecto,
                    'avisoTarea': 'Debe contener un nombre.',
                    'categorias': CategoriasProyecto,
                    'Tareas': tareas,
                    'Proyecto': proyectoDB,
                    'usuario': miembroAdmin,
                    'miembros': miembros,
                })
                
            if not re.fullmatch("^[a-zA-Z0-9\s]{1,}$", datos['DescripcionTarea']):
                return render(request, 'proyecto/tableros.html', {
                    "id_proyecto": id_proyecto,
                    'miembros': miembros,
                    'categorias': CategoriasProyecto,
                    'Tareas': tareas,
                    'Proyecto': proyectoDB,
                    'usuario': miembroAdmin,
                    'avisoTarea': 'Debe contener una descripcion.'
                })
                
            try:
                
                CategoriaDB = categorias.objects.get(pk=datos['CategoriaTarea'])
                ProyectoDB = Proyectos.objects.get(pk=id_proyecto)
                usuarioDB = Usuarios.objects.get(correo=datos['AsignacionTarea'])
                
                crearTarea = TareasDB(nombre=datos['TituloTarea'], descripcion=datos['DescripcionTarea'], prioridad=datos['PrioridadTarea'], categoria=CategoriaDB)
                
                tarea_proyectoDB = tareas_proyecto(id_tarea=crearTarea, id_proyecto=ProyectoDB, usuario=usuarioDB)
                
                crearTarea.save()
                tarea_proyectoDB.save()
                
                print('tarea creada')
            except Exception as Error:
                
                print(f"Error: {Error}")
            

    
    return render(request, 'proyecto/tableros.html', {
        "id_proyecto": id_proyecto,
        'miembros': miembros,
        'categorias': CategoriasProyecto,
        'Tareas': tareas,
        'Proyecto': proyectoDB,
        'usuario': miembroAdmin,
    })


def TableroEstadistica (request, id_proyecto):
    print(id_proyecto)
    
    return render(request, 'proyecto/Estadisticas.html', {
        "id_proyecto": id_proyecto
    })

def EditarTareaProyecto(request, id_proyecto, id_tarea):
    
    return render(request, 'proyecto/editarTarea.html', {
        "id_proyecto": id_proyecto
    })

def Perfil(request):
    
    
    # Para que no entre a esta ruta si no esta logeado
    if not request.user.is_authenticated:
        
        return redirect('Inicio')
    
    userProyectos = miembros_proyecto.objects.filter(usuario=request.user)
    
    # Para crear un Proyecto nuevo
    if request.method == 'POST':
        
        
        if not request.user.is_authenticated:
            return render(request, 'perfil.html', {
                'proyectos': userProyectos,
                'admin': request.user.is_staff,
            })
        
        datos = request.POST
        
        if re.fullmatch(r'^\s+|^\s*$', datos['NombreProyecto']):
            return render(request, 'perfil.html', {
                'proyectos': userProyectos,
                'admin': request.user.is_staff,
                'aviso': 'No se puede crear con solamente espacios'
            })
        
        if re.fullmatch('^[a-zA-Z0-9\s]{3,}$', datos['NombreProyecto']):
            
            try:
                proyecto = Proyectos(nombre=datos['NombreProyecto'])
                
                creador = miembros_proyecto(id_proyecto=proyecto, usuario=request.user, is_admin=True)

            except:
                return render(request, 'perfil.html', {
                    'proyectos': userProyectos,
                    'admin': request.user.is_staff,
                    'aviso': 'Hubo un problema con el servidor'
                })
            
            proyecto.save()
            creador.save()
            
            for idCategoria in range(1,5):
                
                categoriaPredeterminada = categorias.objects.get(pk=idCategoria)
                
                CategoriaProyecto = categorias_proyecto(id_proyecto=proyecto, id_categoria=categoriaPredeterminada)
                
                CategoriaProyecto.save()
            
        else:
            return render(request, 'perfil.html', {
                'proyectos': userProyectos,
                'admin': request.user.is_staff,
                'aviso': 'Solamente letras, numeros y espacio'
            })
    
        
    
    
    return render(request, 'perfil.html', {
        'proyectos': userProyectos,
        'admin': request.user.is_staff,
    })




def PanelAdmin(request):
    
    # Para que no entre a esta ruta si no esta logeado
    if not request.user.is_authenticated:
        
        return redirect('Inicio')
    
    return render(request, 'admin.html')

# Se encarga Miguel

def ProyectosAdmin(request):
    
    # Para que no entre a esta ruta si no esta logeado
    if not request.user.is_authenticated:
        
        return redirect('Inicio')
    
    return render(request, 'admin/ProyectosAdmin.html')


def UsuariosAdmin(request):
    
    # Para que no entre a esta ruta si no esta logeado
    if not request.user.is_authenticated:
        
        return redirect('Inicio')
    
    return render(request, 'admin/UsuariosAdmin.html')