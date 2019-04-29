from django.shortcuts import render
def index(request):
	return render(request,'integrantes/index.html')

def catalogo(request):
	return render(request,'integrantes/catalogo.html')

def contacto(request):
	return render(request,'integrantes/contacto.html')
# Create your views here.
