from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contacto/enviar/", views.enviar_mensaje, name="enviar_mensaje"),
]
