from django.urls import path
from . import views 

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("login", views.Login, name='Login'),
    path("registro", views.Registro, name='Registro'),
    path("proyecto", views.Proyectos, name='Proyectos'),
]
