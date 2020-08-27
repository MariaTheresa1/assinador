from django.urls import path
from . import views

urlpatterns = [
    path('', views.assinador, name= 'assinador'), 
    path('verificador', views.verificador, name= 'verificador'), 
    path('gerar-chaves', views.gerar_chaves, name= 'gerar_chaves'), 
    path('baixar-chave-publica/<chave>', views.baixar_chave_publica, name= 'baixar_chave_publica'),
    path('baixar-chave-privada/<chave>', views.baixar_chave_privada, name= 'baixar_chave_privada'),
]
