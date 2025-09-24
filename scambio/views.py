from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect
from .forms import *

# Create your views here.


def home(request):
    #print(DocumentiCliente.objects.get(utente=request.user))
    return render(request, 'home.html')

def addItem(request):
    if request.method == 'POST':
        form = UploadItemForm(request.POST, request.FILES, user=request.user)
        print(form.errors)
        if form.is_valid():
            obj = form.save(commit=False)
            # se Oggetto ha un campo owner:
            obj.proprietario = request.user
            obj.save()
            form.save_m2m()
            # redirect o risposta
            return redirect('home')
    else:
        form = UploadItemForm(user=request.user)

    return render(request, 'aggiungiItem.html', {'form': form})

def prodotto(request,id):
    try:
        item=Oggetto.objects.get(id=id)
    except Oggetto.DoesNotExist:
        return redirect("home")
    
    return render(request, 'prodotto.html',{'item':item})