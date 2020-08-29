from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

def assinador(request):
    return render(request, "assinador.html", {})

def verificador(request):
    return render(request, "verificador.html", {})

def gerar_chaves(request):
    try: 
        chave = RSA.generate(2048)
        chave_privada = chave.export_key().hex()
        chave_publica = chave.publickey().export_key().hex()
        print(chave_privada)
        print(chave_publica)
        return JsonResponse({'sucesso':True, 'chaveprivada': chave_privada, 'chavepublica': chave_publica}, safe= False)
    except:
        return JsonResponse({'sucesso':False}, safe= False)

@csrf_protect
def assinar_mensagem(request):
    try:
        chaveprivada = bytes.fromhex(request.POST.get("chaveprivada"))
        tipoassinatura= request.POST.get("tipoassinatura")
        if(tipoassinatura=="texto"):
            mensagem = str.encode(request.POST.get("texto"))
        else:
            mensagem = request.FILES.get("arquivo").read()
        
        chave = RSA.import_key(chaveprivada)
        h = SHA256.new(mensagem)
        assinatura = pkcs1_15.new(chave).sign(h)
        mensagem_assinada = assinatura.hex()
        print(assinatura)

        return render(request,"assinador.html",{'sucesso':True, 'chaveprivada': request.POST.get("chaveprivada"), 'chavepublica': request.POST.get("chavepublica"), 'mensagemassinada':mensagem_assinada})
    except:
        return render(request,"assinador.html",{'sucesso':False})

@csrf_protect
def verificar_assinatura(request):
    try:
        tipocertificado= request.POST.get("tipocertificado")
        tipomensagemclaro= request.POST.get("tipomensagemclaro")
        tipomensagem= request.POST.get("tipomensagem")

        if(tipocertificado=="certificadotexto"):
            chavepublica = bytes.fromhex(request.POST.get("tipocertificadotexto"))
        else:
            arquivo = request.FILES['tipocertificadoarquivo']
            chavepublica = ''

            for linha in arquivo:
                chavepublica = chavepublica + linha.decode()

            chavepublica = bytes.fromhex(chavepublica)
        print(chavepublica)

        if(tipomensagemclaro=="mensagemclarotexto"):
            mensagemclaro = str.encode(request.POST.get("tipomensagemclarotexto"))
        else:
            arquivo = request.FILES['tipomensagemclaroarquivo']
            mensagemclaro = ''

            for linha in arquivo:
                mensagemclaro = mensagemclaro + linha.decode()

            mensagemclaro = str.encode(mensagemclaro)
        print(mensagemclaro)

        if(tipomensagem=="mensagemtexto"):
            mensagemassinada = bytes.fromhex(request.POST.get("tipomensagemtexto"))
        else:
            arquivo = request.FILES['tipomensagemarquivo']
            mensagemassinada = ''

            for linha in arquivo:
                mensagemassinada = mensagemassinada + linha.decode()

            mensagemassinada = bytes.fromhex(mensagemassinada)
        print(mensagemassinada)

        chave = RSA.import_key(chavepublica)
        h = SHA256.new(mensagemclaro)
        pkcs1_15.new(chave).verify(h, mensagemassinada)

        return render(request,"verificador.html",{'sucesso':True})
    except (ValueError, TypeError):
        return render(request,"verificador.html",{'sucesso':False})
