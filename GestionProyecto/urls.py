from django.urls import path
from . import views 

urlpatterns = [
    path("", views.inicio, name="Inicio"),
    path("login", views.Login, name='Login'),
    path("registro", views.Registro, name='Registro'),
    path("cerrarSesion", views.CerrarSesion, name='CerrarSesion'),
    path("perfil", views.Perfil, name='Perfil'),
    path("<int:id_proyecto>/tablero", views.TableroProyecto, name='ProyectoTablero'),
    path("<int:id_proyecto>/estadistica", views.TableroEstadistica, name='ProyectoEstadistica'),
    path("<int:id_proyecto>/<int:id_tarea>/EditarTarea", views.EditarTareaProyecto, name="EditarTarea"),
    path("panelAdmin/proyectos", views.ProyectosAdmin, name='PAdminProyectos'),
    path("panelAdmin/usuarios", views.UsuariosAdmin, name='PAdminUsuarios'),
]
