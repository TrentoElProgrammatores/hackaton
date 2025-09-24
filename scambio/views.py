from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect

# Create your views here.


def home(request):
    #print(DocumentiCliente.objects.get(utente=request.user))
    return render(request, 'home.html')

def addItem(request):
    return render(request, 'aggiungiItem.html')