from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect
from .forms import *
from .models import *

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
    data={'item':item}
    categoria=OggettoCategoria.objects.filter(oggetto=item).first()
    data.update({'categoria':categoria})
    scambio=MerceScambiata.objects.filter(oggetto=item)
    data.update({'scambio':scambio})
    return render(request, 'prodotto.html',data)

def addScatola(request):
    if request.method == 'POST':
        form = UploadScatolaForm(request.POST, request.FILES, user=request.user)
        print(form.errors)
        if form.is_valid():
            scatola = form.save(commit=False)

            # Se il modello Scatola ha un campo owner e non lo gestisci già nel form.save()
            # scatola.owner = request.user

            scatola.save()
            form.save_m2m()  # serve solo se hai campi ManyToMany (puoi anche toglierlo se non ne hai)

            # 🔁 Dopo il salvataggio puoi reindirizzare dove preferisci:
            return redirect('home')  # oppure 'lista_scatole', 'dashboard', ecc.

    else:
        form = UploadScatolaForm(user=request.user)

    return render(request, 'aggiungiScatola.html', {'form': form})
