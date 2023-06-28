from django.urls import path
from Recursos_Humanos import views

urlpatterns = [
    path('cadastrar_funcionario', views.cadastrar_funcionario),
    path('buscar_funcionarios', views.buscar_funcionarios),
]
