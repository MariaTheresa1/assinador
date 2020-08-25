from django.shortcuts import render, HttpResponse

def assinador(request):
    return HttpResponse("Olá mundo!")