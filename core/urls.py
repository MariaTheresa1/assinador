from django.urls import path
from . import views

urlpatterns = [
    path('', views.assinador, name= 'assinador'), 
    path('verificador', views.verificador, name= 'verificador'), 
    path('gerar-chaves', views.gerar_chaves, name= 'gerar_chaves'), 
    path('assinar-mensagem', views.assinar_mensagem, name="assinar_mensagem"),
    path('verificar-assinatura', views.verificar_assinatura, name="verificar_assinatura")
]
