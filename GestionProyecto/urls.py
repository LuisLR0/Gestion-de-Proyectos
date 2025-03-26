from django.urls import path
from . import views 


urlpatterns = [
    path("", views.inicio, name="Inicio"),
    path("login", views.Login, name='Login'),
    path("registro", views.Registro, name='Registro'),
    path("cerrarSesion", views.CerrarSesion, name='CerrarSesion'),
    path("perfil", views.Perfil, name='Perfil'),
    path("<int:id_proyecto>/tablero", views.TableroProyecto, name='ProyectoTablero'),
    path("<int:id_proyecto>/EliminarProyecto", views.EliminarProyecto, name='EliminarProyecto'),
    path("<int:id_categoria>/<int:id_proyecto>/EliminarCategoria", views.EliminarCategoriaProyecto, name='EliminarCategoria'),
    path("<int:id_miembro>/<int:id_proyecto>/EliminarMiembro", views.EliminarMiembroProyecto, name='EliminarMiembro'),
    path("<int:id_proyecto>/estadistica", views.TableroEstadistica, name='ProyectoEstadistica'),
    path("<int:id_proyecto>/<int:id_tarea>/EditarTarea", views.EditarTareaProyecto, name="EditarTarea"),
    path("<int:id_proyecto>/<int:id_tarea>/<int:id_categoria>/dropTarea", views.dropTareaCategoria, name="dropCategoria"),
    path("<int:id_tarea>/EliminarTarea/<int:id_proyecto>", views.EliminarTarea, name="EliminarTarea"),
    path("panelAdmin/proyectos", views.ProyectosAdmin, name='PAdminProyectos'),
    path("panelAdmin/usuarios", views.UsuariosAdmin, name='PAdminUsuarios'),
    path("panelAdmin/<str:correoAdmin>/usuarios", views.deleteUsuarioAdmin, name='PAdminDeleteUsuarios'),
]
