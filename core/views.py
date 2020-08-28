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
        return JsonResponse({'sucesso':True, 'chaveprivada': chave_privada, 'chavepublica': chave_publica}, safe= False)
    except:
        return JsonResponse({'sucesso':False}, safe= False)

@csrf_protect
def assinar_mensagem(request):
    try:
        print(request.POST)
        chaveprivada = bytes.fromhex(request.POST.get("chaveprivada"))
        tipoassinatura= request.POST.get("tipoassinatura")
        if(tipoassinatura=="texto"):
            mensagem = str.encode(request.POST.get("texto"))
        else:
            mensagem = request.FILES.get("arquivo").read()
        
        print(chaveprivada)
        chave = RSA.import_key(chaveprivada)
        h = SHA256.new(mensagem)
        assinatura = pkcs1_15.new(chave).sign(h)
        mensagem_assinada = assinatura.hex()

        return render(request,"assinador.html",{'sucesso':True, 'chaveprivada': request.POST.get("chaveprivada"), 'chavepublica': request.POST.get("chavepublica"), 'mensagemassinada':mensagem_assinada})
    except:
        return render(request,"assinador.html",{'sucesso':False})

@csrf_protect
def verificar_assinatura(request):
        #try:
        print(request.POST)
        chavepublica = bytes.fromhex(request.POST.get("chavepublica"))

        tipocertificado= request.POST.get("tipocertificado")
        tipomensagemclaro= request.POST.get("tipomensagemclaro")
        tipomensagem= request.POST.get("tipomensagem")

        if(tipocertificado=="certificadotexto"):
            chavepublica = str.encode(request.POST.get("tipocertificadotexto"))
        else:
            chavepublica = request.FILES.get("tipocertificadoarquivo").read()

        if(tipomensagemclaro=="mensagemclarotexto"):
            mensagemclaro = str.encode(request.POST.get("tipomensagemclarotexto"))
        else:
            mensagemclaro = request.FILES.get("tipomensagemclaroarquivo").read()

        if(tipomensagem=="mensagemtexto"):
            mensagemassinada = str.encode(request.POST.get("tipomensagemtexto"))
        else:
            mensagemassinada = request.FILES.get("tipomensagemarquivo").read()
        
        chave = RSA.import_key(chavepublica)
        h = SHA256.new(mensagemclaro)
        pkcs1_15.new(chave).verify(h, mensagemassinada)

        return render(request,"verificador.html",{'sucesso':True})
        #except:
        return render(request,"verificador.html",{'sucesso':False})

'''
message = b'Hello, World!'

key = RSA.import_key(private_key)
h = SHA256.new(message)
signature = pkcs1_15.new(key).sign(h)
#print(h)
#print(signature.decode('utf-8', 'ignore'))
#print(signature)
#print(signature.hex())
#print(bytes.fromhex(signature.hex())


key = RSA.import_key(public_key)
h = SHA256.new(message)

try:
    pkcs1_15.new(key).verify(h, signature)
    print("A assinatura é válida.")
except (ValueError, TypeError):
    print("A assinatura não é válida.")
    '''     