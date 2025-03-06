from django.urls import path
from . import views 

urlpatterns = [
    path("", views.inicio, name="Inicio"),
    path("login", views.Login, name='Login'),
    path("registro", views.Registro, name='Registro'),
    path("perfil", views.Perfil, name='Perfil'),
    path("proyecto/tablero", views.TableroProyecto, name='ProyectoTablero'),
    path("proyecto/estadistica", views.TableroEstadistica, name='ProyectoEstadistica'),
    path("panelAdmin/proyectos", views.ProyectosAdmin, name='PAdminProyectos'),
    path("panelAdmin/usuarios", views.UsuariosAdmin, name='PAdminUsuarios'),
]
