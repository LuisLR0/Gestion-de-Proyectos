from django.urls import path
from . import views 

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("Perfil", views.perfil, name='perfil')
]
