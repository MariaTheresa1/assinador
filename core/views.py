from django.shortcuts import render, HttpResponse

def assinador(request):
    return render(request, "assinador.html", {})

def verificador(request):
    return render(request, "verificador.html", {})