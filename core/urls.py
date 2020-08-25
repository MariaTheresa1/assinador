from django.urls import path
from . import views

urlpatterns = [
    path('', views.assinador, name= 'assinador'), 
    path('verificador', views.verificador, name= 'verificador'), 
]
