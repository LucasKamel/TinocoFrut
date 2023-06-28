from django.urls import path
from Financeiro import views

urlpatterns = [
    path('registrar_compra', views.comprar),
    path('registrar_venda', views.vender),
    path('relatorio_vendas', views.relatorio_vendas),
    path('relatorio_compras', views.relatorio_compras),
]
