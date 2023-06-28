from django.urls import path
from Produtos import views

urlpatterns = [
    path('cadastrar', views.cadastrar_produto),
]
