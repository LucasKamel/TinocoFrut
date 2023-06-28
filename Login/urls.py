from django.urls import path
from Login import views

urlpatterns = [
    path('logar', views.realizar_login),
]
