from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.db.models import Count, Case, When, Value
from .models import Usuarios, Proyectos, miembros_proyecto, tareas_proyecto, tareas as TareasDB, categorias, categorias_proyecto


from django.http import HttpResponse
from django.template.loader import render_to_string # para convertir el html en string
from django.utils import timezone
from xhtml2pdf import pisa
import io

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
                
                CategoriaProyecto = categorias_proyecto(id_proyecto=proyecto, id_categoria=categoriaPredeterminada, indice=idCategoria)
                
                CategoriaProyecto.save()
 
            
        else:
            return render(request, 'inicio.html', {
                'aviso': 'Solamente letras, numeros y espacio'
            })
        
    if request.user.is_authenticated:
        
        userProyectos = miembros_proyecto.objects.filter(usuario=request.user)
        
        datosProyecto = {}
        
        for proy in userProyectos:
            
            datosProyecto[proy.id_proyecto] = {
                'TareasTotal': tareas_proyecto.objects.filter(id_proyecto=proy.id_proyecto).count(), 
                'MiembrosTotal': miembros_proyecto.objects.filter(id_proyecto=proy.id_proyecto).count(),
            }
        
        return render(request, 'inicio.html', {
            'proyectos': userProyectos,
            'datosProyecto': datosProyecto.items(),
        })
    else:
        return render(request, 'inicio.html')

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
            
            return render(request, "login.html", {'aviso': "Correo o Contraseña Incorrecta"})
    
    return render(request, "login.html")

def Registro (request):
    
    if request.user.is_authenticated:
        
        return redirect('Inicio')
    
    if request.method == 'POST':
        datos = request.POST
        
        print(datos)
        
        for indice, valor in datos.items():
            
            if re.fullmatch(r'^\s+|^\s*$', valor):
                return render(request, 'registro.html', {
                    'aviso': "Comprueba de que ninguna campo contenga espacios."
                })
            
        if not re.fullmatch(r'^[ñÑa-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', datos['correo']):
            return render(request, 'registro.html', {
                'aviso': "Correo Invalido"
            })
            
        if not re.fullmatch(r'^[a-zA-ZñÑ\s]{3,}$', datos['nombres']):
            return render(request, 'registro.html', {
                'aviso': "Nombre Invalido"
            })
        if not re.fullmatch(r'^[a-zA-ZñÑ\s]{3,}$', datos['apellidos']):
            return render(request, 'registro.html', {
                'aviso': "Apellido Invalido"
            })
            
        verifyCorreo = Usuarios.objects.filter(correo=datos['correo'])
        
        if verifyCorreo:
            return render(request, 'registro.html', {
                'aviso': "Correo ya registrado"
            })
        
        try:
            correo = datos['correo']
            nombres = datos['nombres']
            apellidos = datos['apellidos']
            contraseña = datos['contraseña']
            
            Usuarios.objects.create_user(correo=correo, nombre=nombres, apellido=apellidos, password=contraseña)
            
            return redirect('Login')
        except:
            return redirect('Registro')
    
    return render(request, 'registro.html')

def CerrarSesion (request):
    
    # Para que no entre a esta ruta si no esta logeado
    if not request.user.is_authenticated:
        
        return redirect('Inicio')
    
    logout(request)
    return redirect('Inicio')

def TableroProyecto (request, id_proyecto):
    
    # Para que no entre a esta ruta si no esta logeado
    if not request.user.is_authenticated:
        
        return redirect('Inicio')
    
    miembros = miembros_proyecto.objects.filter(id_proyecto=id_proyecto)
    CategoriasProyecto = categorias_proyecto.objects.filter(id_proyecto=id_proyecto).order_by('indice')
    
    ordenPrioridad = Case(
        When(id_tarea__prioridad='ALTA', then=1),
        When(id_tarea__prioridad='MEDIA', then=2),
        When(id_tarea__prioridad='BAJA', then=3)
    )
    
    tareas = tareas_proyecto.objects.filter(id_proyecto=id_proyecto).order_by(ordenPrioridad)
        
    proyectoDB = Proyectos.objects.get(pk=id_proyecto)
    
    miembroAdmin = None
    
    if not request.user.is_staff:
        
        try:
            miembroAdmin = miembros_proyecto.objects.get(id_proyecto=id_proyecto, usuario=request.user)
        except:
            return redirect('Inicio')
    else:
        
        miembro = False
        
        try:
            miembro = miembroAdmin = miembros_proyecto.objects.get(id_proyecto=id_proyecto, usuario=request.user)
        except:
            pass
        
        miembroAdmin = {
            'is_admin': miembro.is_admin if miembro else False,
            'staff': True,
            'usuario': miembro.usuario if miembro else None,
        }
    
    if request.method == "POST":
        
        tipoPost = request.POST.get('tipoPost')
        
        datos = request.POST
        
        if tipoPost == "CrearTarea":
            
            print(datos)

            if not re.fullmatch("^[a-zA-Z0-9ñÑ\s]{1,}$", datos['DescripcionTarea']):
                return render(request, 'proyecto/tableros.html', {
                    "id_proyecto": id_proyecto,
                    'categorias': CategoriasProyecto,
                    'Tareas': tareas,
                    'Proyecto': proyectoDB,
                    'usuario': miembroAdmin,
                    'miembros': miembros,
                    'avisoTarea': 'Debe contener un nombre.',
                })
                
            if not re.fullmatch("^[a-zA-Z0-9ñÑ\s]{1,}$", datos['DescripcionTarea']):
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
                
                return redirect('ProyectoTablero', id_proyecto)
            except Exception as Error:
                
                print(f"Error: {Error}")
        
        elif tipoPost == "CrearColumna":

            if not re.fullmatch("^[a-zA-Z0-9\s]{1,}$", datos['NombreColumna']):
                return render(request, 'proyecto/tableros.html', {
                    "id_proyecto": id_proyecto,
                    'miembros': miembros,
                    'categorias': CategoriasProyecto,
                    'Tareas': tareas,
                    'Proyecto': proyectoDB,
                    'usuario': miembroAdmin,
                    'avisoColumna': 'Debe contener una Nombre.'
                })
                
            
            numerosCategorias = None
            
            try:
                numerosCategorias = [
                    categoria.indice for categoria in categorias_proyecto.objects.filter(id_proyecto_id=id_proyecto)
                ]
            except:
                pass
            
            indice = max(numerosCategorias) + 1 if numerosCategorias else 1
                
            categoriaNueva = None
            
            try:
                
                categoriaNueva = categorias.objects.get(nombre=datos['NombreColumna'])
                CategoriaProyecto = categorias_proyecto(id_proyecto_id=id_proyecto, id_categoria=categoriaNueva, indice=indice)
                
            except categorias.DoesNotExist:
                
                categoriaNueva = categorias(nombre=datos['NombreColumna'])
                CategoriaProyecto = categorias_proyecto(id_proyecto_id=id_proyecto, id_categoria=categoriaNueva, indice=indice)
                
                
            except Exception as Error:
                print(f"Error: {Error}")
            
            if categoriaNueva:
                categoriaNueva.save()
                CategoriaProyecto.save()
                
                return redirect('ProyectoTablero', id_proyecto)
                
        elif tipoPost == "actualizarNombreProyecto":
            
            if not request.user.is_staff:
                if not miembroAdmin.is_admin:
                    return render(request, 'proyecto/tableros.html', {
                        "id_proyecto": id_proyecto,
                        'miembros': miembros,
                        'categorias': CategoriasProyecto,
                        'Tareas': tareas,
                        'Proyecto': proyectoDB,
                        'usuario': miembroAdmin,
                    })
                
            
            
            if not re.fullmatch("^[a-zA-Z0-9\s]{1,}$", datos['NombreProyecto']):
                return render(request, 'proyecto/tableros.html', {
                    "id_proyecto": id_proyecto,
                    'miembros': miembros,
                    'categorias': CategoriasProyecto,
                    'Tareas': tareas,
                    'Proyecto': proyectoDB,
                    'usuario': miembroAdmin,
                    'avisoOpcion': 'Debe contener una Nombre.'
                })
                
            try:
                
                nombreProyecto = Proyectos.objects.get(pk=id_proyecto)
                
                nombreProyecto.nombre = datos['NombreProyecto']
                
                nombreProyecto.save()
                
                return redirect('ProyectoTablero', id_proyecto)
            
            except Exception as Error:
                print(f"Error: {Error}")
                
        elif tipoPost == "IndiceColumna":
            CategoriaIndice = categorias_proyecto.objects.get(pk=datos['idCategoriaProyecto'])
            CategoriaIndice.indice = datos['indiceCategoria']
            CategoriaIndice.save()
            
            return redirect('ProyectoTablero', id_proyecto)
            
        elif tipoPost == "invitarMiembro":
            if not request.user.is_staff:
                if not miembroAdmin.is_admin:
                    return render(request, 'proyecto/tableros.html', {
                        "id_proyecto": id_proyecto,
                        'miembros': miembros,
                        'categorias': CategoriasProyecto,
                        'Tareas': tareas,
                        'Proyecto': proyectoDB,
                        'usuario': miembroAdmin,
                    })
            
            usuarioInvitar= None
            
            try:
                
                usuarioInvitar = Usuarios.objects.get(correo=datos['correoMiembro'])
                
            except:
                # Aca va un aviso de que no se encontro el correo
                return render(request, 'proyecto/tableros.html', {
                    "id_proyecto": id_proyecto,
                    'miembros': miembros,
                    'categorias': CategoriasProyecto,
                    'Tareas': tareas,
                    'Proyecto': proyectoDB,
                    'usuario': miembroAdmin,
                    'avisoInvitar': 'No se encontro el correo.'
                })
            
            if usuarioInvitar:
                miembroInvitar = miembros_proyecto(id_proyecto_id=id_proyecto, usuario=usuarioInvitar)
                miembroInvitar.save()
                return redirect('ProyectoTablero', id_proyecto)
            
            

    
    return render(request, 'proyecto/tableros.html', {
        "id_proyecto": id_proyecto,
        'miembros': miembros,
        'categorias': CategoriasProyecto,
        'Tareas': tareas,
        'Proyecto': proyectoDB,
        'usuario': miembroAdmin,
    })

def TableroEstadistica (request, id_proyecto):
    
    if not request.user.is_staff:
        
        try:
            miembroAdmin = miembros_proyecto.objects.get(id_proyecto=id_proyecto, usuario=request.user)
        except:
            return redirect('Inicio')

    
    CategoriasProyecto = categorias_proyecto.objects.filter(id_proyecto=id_proyecto).order_by('indice')
    
    tareas = {}
    
    for categoria in CategoriasProyecto:
        tareas[f"{categoria.id_categoria.nombre}"] = tareas_proyecto.objects.filter(id_proyecto=id_proyecto).aggregate(
            valor=Count(Case(When(id_tarea__categoria_id=categoria.id_categoria.pk, then=Value(1)))),
        )
    
    tareasTotal = tareas_proyecto.objects.filter(id_proyecto=id_proyecto).count()
    
    return render(request, 'proyecto/Estadisticas.html', {
        "id_proyecto": id_proyecto,
        'categorias': CategoriasProyecto,
        'Tareas': tareas.items(),
        'tareasTotal': tareasTotal,
    })
    
def EliminarMiembroProyecto(request, id_miembro, id_proyecto):

    
    if not request.user.is_staff:
        
        try:
            usuarioAdmin = miembros_proyecto.objects.get(id_proyecto_id=id_proyecto, usuario=request.user)
        except:
            return redirect('Inicio')
        
        
        if not usuarioAdmin.is_admin:
            return redirect('Inicio')

    try:
        
        MiembroEliminar = miembros_proyecto.objects.get(pk=id_miembro, id_proyecto_id=id_proyecto)
        MiembroEliminar.delete()
        
    except Exception as Error:
        
        print(f"Error: {Error}")
        return redirect('Inicio')
    
    return redirect('ProyectoTablero', id_proyecto)

def EliminarCategoriaProyecto(request, id_categoria, id_proyecto):
    
    if not request.user.is_staff:
        try:
            miembro = miembros_proyecto.objects.get(id_proyecto_id=id_proyecto, usuario=request.user)
        except:
            return redirect('Inicio')

    tareas = tareas_proyecto.objects.filter(id_proyecto_id=id_proyecto)
    
    CategoriaIndice = categorias_proyecto.objects.get(pk=id_categoria)
    
    for tarea in tareas:
        
        if tarea.id_tarea.categoria == CategoriaIndice.id_categoria:
            borrarTarea = tareas_proyecto.objects.get(pk=tarea.pk)
            borrarTarea.delete()
    
    CategoriaIndice.delete()
    
    return redirect('ProyectoTablero', id_proyecto)
      
def EliminarProyecto(request, id_proyecto):
    # No se pueda usar si no es admin del proyecto
    
    if not request.user.is_staff:
        miembros = miembros_proyecto.objects.get(id_proyecto=id_proyecto, usuario=request.user)
        
        if not miembros.is_admin:
            return redirect('Inicio')
    
    
    proyectoEliminar = Proyectos.objects.get(pk=id_proyecto)
    
    
    proyectoEliminar.delete()
    
    return redirect('Inicio')

def EliminarTarea(request, id_tarea, id_proyecto):
    # No se pueda usar si no es miembro del proyecto
    if not request.user.is_staff:
        try:
            miembro = miembros_proyecto.objects.get(id_proyecto_id=id_proyecto, usuario=request.user)
        except:
            return redirect('Inicio')
    
    tareaEliminar = TareasDB.objects.get(id_tarea=id_tarea)
    
    tareaEliminar.delete()
    
    return redirect('ProyectoTablero', id_proyecto)

def EditarTareaProyecto(request, id_proyecto, id_tarea):
    
    tareaProyecto = tareas_proyecto.objects.get(id_proyecto=id_proyecto, id_tarea=id_tarea)
    miembros = miembros_proyecto.objects.filter(id_proyecto=id_proyecto)
    CategoriasProyecto = categorias_proyecto.objects.filter(id_proyecto=id_proyecto)
    
    datos = None
    
    if request.method == "POST":
        
        
        datos = request.POST
            
        print(datos)

        if not re.fullmatch(r"^[a-zA-Z0-9ñÑ\s]{1,}$", datos['DescripcionTarea']):
            return render(request, 'proyecto/tableros.html', {
                'avisoTarea': 'Debe contener un nombre.',
                "id_proyecto": id_proyecto,
                "datosTarea": tareaProyecto.id_tarea,
                "miembroAsignado": tareaProyecto.usuario,
                "miembros": miembros,
                "categorias": CategoriasProyecto,
            })
            
        if not re.fullmatch(r"^[a-zA-Z0-9ñÑ\s]{1,}$", datos['DescripcionTarea']):
            return render(request, 'proyecto/tableros.html', {
                "id_proyecto": id_proyecto,
                "datosTarea": tareaProyecto.id_tarea,
                "miembroAsignado": tareaProyecto.usuario,
                "miembros": miembros,
                "categorias": CategoriasProyecto,
                'avisoTarea': 'Debe contener una descripcion.'
            })
            
        try:
            
            CategoriaDB = categorias.objects.get(pk=datos['CategoriaTarea'])
            usuarioDB = Usuarios.objects.get(correo=datos['AsignacionTarea'])
            
            TareaActualizar = TareasDB.objects.get(pk=id_tarea)
            Tarea_ProyectoActualizar = tareas_proyecto.objects.get(id_tarea=id_tarea)
            
            TareaActualizar.nombre = datos['TituloTarea']
            TareaActualizar.descripcion = datos['DescripcionTarea']
            TareaActualizar.prioridad = datos['PrioridadTarea']
            TareaActualizar.categoria = CategoriaDB
            
            Tarea_ProyectoActualizar.usuario = usuarioDB
            
            
            TareaActualizar.save()
            Tarea_ProyectoActualizar.save()
            
            return redirect('ProyectoTablero', id_proyecto)
            

        except Exception as Error:
            
            print(f"Error: {Error}")

    return render(request, 'proyecto/editarTarea.html', {
        "id_proyecto": id_proyecto,
        "datosTarea": tareaProyecto.id_tarea,
        "miembroAsignado": tareaProyecto.usuario,
        "miembros": miembros,
        "categorias": CategoriasProyecto,
    })

def dropTareaCategoria(request, id_proyecto, id_tarea, id_categoria):
    
    if not request.user.is_staff:
        # No se pueda usar si no es miembro del proyecto
        try:
            miembro = miembros_proyecto.objects.get(id_proyecto_id=id_proyecto, usuario=request.user)
        except:
            return redirect('Inicio')
    
    
    try:
        CategoriaDB = categorias.objects.get(pk=id_categoria)
        tareaActualizar = TareasDB.objects.get(id_tarea=id_tarea)
        
        tareaActualizar.categoria = CategoriaDB
        
        tareaActualizar.save()
    except:
        return redirect('ProyectoTablero', id_proyecto)
 
    return redirect('ProyectoTablero', id_proyecto)

def Perfil(request):
    
    
    # Para que no entre a esta ruta si no esta logeado
    if not request.user.is_authenticated:
        
        return redirect('Inicio')
    
    userProyectos = miembros_proyecto.objects.filter(usuario=request.user)
    usuario = Usuarios.objects.get(correo=request.user)
    
    totalProyectos = miembros_proyecto.objects.filter(usuario=request.user).count()
    totalTareas = tareas_proyecto.objects.filter(usuario_id=request.user).count()
    
    datosProyecto = {}
        
    for proy in userProyectos:
        
        datosProyecto[proy.id_proyecto] = {
            'TareasTotal': tareas_proyecto.objects.filter(id_proyecto=proy.id_proyecto).count(), 
            'MiembrosTotal': miembros_proyecto.objects.filter(id_proyecto=proy.id_proyecto).count(),
        }
        
    
    # Para crear un Proyecto nuevo
    if request.method == 'POST':
        
        datos = request.POST
        
        if re.fullmatch(r'^\s+|^\s*$', datos['NombreProyecto']):
            return render(request, 'perfil.html', {
                'proyectos': userProyectos,
                'admin': request.user.is_staff,
                'usuario': usuario,
                'totalProyectos': totalProyectos,
                'totalTareas': totalTareas,
                'datosProyecto': datosProyecto.items(),
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
                    'usuario': usuario,
                    'totalProyectos': totalProyectos,
                    'totalTareas': totalTareas,
                    'datosProyecto': datosProyecto.items(),
                    'aviso': 'Hubo un problema con el servidor'
                })
            
            proyecto.save()
            creador.save()
            
            for idCategoria in range(1,5):
                
                categoriaPredeterminada = categorias.objects.get(pk=idCategoria)
                
                CategoriaProyecto = categorias_proyecto(id_proyecto=proyecto, id_categoria=categoriaPredeterminada, indice=idCategoria)
                
                CategoriaProyecto.save()
            
            return redirect('Perfil')
            
        else:
            return render(request, 'perfil.html', {
                'proyectos': userProyectos,
                'admin': request.user.is_staff,
                'usuario': usuario,
                'totalProyectos': totalProyectos,
                'totalTareas': totalTareas,
                'datosProyecto': datosProyecto.items(),
                'aviso': 'Solamente letras, numeros y espacio'
            })
    
        
    
    
    return render(request, 'perfil.html', {
        'proyectos': userProyectos,
        'admin': request.user.is_staff,
        'usuario': usuario,
        'totalProyectos': totalProyectos,
        'totalTareas': totalTareas,
        'datosProyecto': datosProyecto.items(),
    })

def ProyectosAdmin(request):
    
    # Para que no entre a esta ruta si no esta logeado
    if not request.user.is_authenticated and not request.user.is_staff:
        
        return redirect('Inicio')
    
    allProyectos = miembros_proyecto.objects.values('id_proyecto_id').distinct()
    
    proyectos = []
    
    for proyecto in allProyectos:
        search = miembros_proyecto.objects.filter(id_proyecto_id=proyecto['id_proyecto_id']).first()
        proyectos.append(search)
    
        
    datosProyecto = {}
    
    print(proyectos)
    for proy in proyectos:
        
        datosProyecto[proy.id_proyecto] = {
            'TareasTotal': tareas_proyecto.objects.filter(id_proyecto=proy.id_proyecto).count(), 
            'MiembrosTotal': miembros_proyecto.objects.filter(id_proyecto=proy.id_proyecto).count(),
        }
    
    
    return render(request, 'admin/ProyectosAdmin.html', {
        'proyectos': proyectos,
        'datosProyecto': datosProyecto.items(),
    })

def UsuariosAdmin(request):
    
    # Para que no entre a esta ruta si no esta logeado
    if not request.user.is_authenticated and not request.user.is_staff:
        
        return redirect('Inicio')
    
    usuarios = Usuarios.objects.filter(is_staff=True)
    
    if request.method == "POST":
        
        datos = request.POST
        
        if re.fullmatch(r'^\s+|^\s*$', datos['correoAdmin']):
            return render(request, 'admin/UsuariosAdmin.html', {
                'userLogin': request.user,
                'usuarios': usuarios,
                'aviso': 'No se puede crear con solamente espacios'
            })
        
        if re.fullmatch(r'^[ñÑa-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', datos['correoAdmin']):
            
            try:
                miembroAdmin = Usuarios.objects.get(correo=datos['correoAdmin'])
                
                if miembroAdmin.is_staff == True:
                    return render(request, 'admin/UsuariosAdmin.html', {
                        'userLogin': request.user,
                        'usuarios': usuarios,
                        'aviso': 'Este correo ya es adminS'
                    })
                
                miembroAdmin.is_staff = True
                
                miembroAdmin.save()
                
            except:
                return render(request, 'admin/UsuariosAdmin.html', {
                    'userLogin': request.user,
                    'usuarios': usuarios,
                    'aviso': 'Correo no registrado'
                })
            
            return redirect('PAdminUsuarios')
            
        else:
            return render(request, 'admin/UsuariosAdmin.html', {
                'userLogin': request.user,
                'usuarios': usuarios,
                'aviso': 'Solamente letras, numeros y espacio'
            })
    
    return render(request, 'admin/UsuariosAdmin.html', {
        'userLogin': request.user,
        'usuarios': usuarios,
    })
    
def deleteUsuarioAdmin(request, correoAdmin):
    
    if not request.user.is_authenticated and not request.user.is_staff:
        
        return redirect('Inicio')
    
    if request.user.correo == correoAdmin:
        print('No te puedes eliminar a ti mismo')
        return redirect('PAdminUsuarios')
        
    try:
        usuarioAdmin = Usuarios.objects.get(correo=correoAdmin)
        
        if usuarioAdmin.is_staff == False:
            return redirect('PAdminUsuarios')
        
        usuarioAdmin.is_staff = False
        
        usuarioAdmin.save()
        
    except:
        return redirect('PAdminUsuarios')
        
    return redirect('PAdminUsuarios')





def generarPDF(request, id_proyecto):
    # Para que no entre a esta ruta si no esta logeado
    if not request.user.is_authenticated:
        return redirect('Inicio')

    
    if not request.user.is_staff:
        
        # Comprobacion si entra un usuario que no esta enel proyecto lo devuelva al inicio
        try:
            miembro = miembros_proyecto.objects.get(id_proyecto=id_proyecto, usuario=request.user)
        except miembros_proyecto.DoesNotExist:
            return redirect('Inicio')

    # Comprobacion si los datos se encuentran, si no se encuentra se envia al inicio
    try:
        CategoriasProyecto = categorias_proyecto.objects.filter(id_proyecto=id_proyecto).order_by('indice')
        tareas = tareas_proyecto.objects.filter(id_proyecto=id_proyecto)
        proyectoDB = Proyectos.objects.get(pk=id_proyecto)
    except (Proyectos.DoesNotExist, categorias_proyecto.DoesNotExist, tareas_proyecto.DoesNotExist) as e:
        print(f"Error: {e}")
        return redirect('Inicio')
    
    
    
    
    
    

    html_string = render_to_string('estadisticaspdf.html', {
        'categorias': CategoriasProyecto,
        'Tareas': tareas,
        'Proyecto': proyectoDB,
        'FechaActual': timezone.now(),
    })

    buffer = io.BytesIO()

    pisa.CreatePDF(
        html_string,
        dest=buffer,
    )

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    return response