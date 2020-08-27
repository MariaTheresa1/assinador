from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

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

def baixar_chave_privada(request, chave):
	filename = 'chave_privada.txt'
	
	response = HttpResponse(chave, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
	
	return response

def baixar_chave_publica(request, chave):
	filename = 'chave_publica.txt'
	
	response = HttpResponse(chave, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
	
	return response

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