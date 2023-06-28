from django.urls import path
from Estoque import views

urlpatterns = [
    path('lista_produtos', views.listar_produtos),
    path('adicionar_estoque', views.adicionar_estoque),
    path('busca/<id>', views.buscar_produto),
]
