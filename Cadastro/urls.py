from django.urls import path
from Cadastro import views

urlpatterns = [
    path('cadastrar_usuario', views.cadastrar),
    path('atualizar_cadastro', views.atualizar_cadastro),
    path('deletar_cadastro', views.deletar_cadastro),
]
