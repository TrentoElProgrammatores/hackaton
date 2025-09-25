from pyexpat.errors import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect
from django.core.mail import send_mail
from .forms import *
from .models import *
from django.contrib.auth import login, logout
from django.conf import settings
import json
from django.http import JsonResponse

# Create your views here.


def home(request):
    #print(DocumentiCliente.objects.get(utente=request.user))
    if request.user.is_authenticated:
        items=Oggetto.objects.all().exclude(location__sede=request.user)
        return render(request, 'home.html',{"items":items})
    else:
        return render(request, 'home.html',{"items":[]})

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
    data.update({'scambi':scambio})
    print("scambio",scambio)
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

def addLocation(request):
    if request.method == 'POST':
        form = UploadLocationForm(request.POST, request.FILES, user=request.user)
        print(form.errors)
        if form.is_valid():
            form.save()  # salva la location e assegna automaticamente sede = user
            return redirect('home')  # reindirizza dove vuoi
    else:
        form = UploadLocationForm(user=request.user)

    return render(request, 'aggiungiLocation.html', {'form': form})


def sedeLogin(request):
    """
    View per il login delle sedi usando il form SedeLoginForm
    """
    if request.method == 'POST':
        form = SedeLoginForm(request, data=request.POST)
        if form.is_valid():
            # Recupera l'utente autenticato
            user = form.get_user()
            login(request, user)  # Logga l'utente nella sessione
            return redirect('home')  # Sostituisci con il nome della tua dashboard
        else:
            messages.error(request, "Username o password non corretti")
    else:
        form = SedeLoginForm()

    return render(request, 'sedeLogin.html', {'form': form})

def sedeLogout(request):
    """
    View per fare il logout dell'utente.
    """
    logout(request)  # termina la sessione dell'utente
    return redirect('sedeLogin')  # reindirizza alla pagina di login


def editProduct(request,id):
    sedi=Sede.objects.all().exclude(id=request.user.id)
    return render(request, 'editProduct.html',{'sedi':sedi,'idprodotto':id})



def confermaPrenotazione(request, item_id):
    item = get_object_or_404(Oggetto, id=item_id)
    utente_loggato = request.user

    # invia email al proprietario
    if item.proprietario.email:
        send_mail(
            subject=f"Nuova prenotazione richiesta per {item.titolo}",
            message=(
                f"Ciao {item.proprietario.nome},\n\n"
                f"L'utente {utente_loggato.nome or utente_loggato.username} "
                f"ha richiesto la prenotazione del tuo oggetto '{item.titolo}'.\n\n"
                f"{settings.DOMINIO}/item/edit/{item.id}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[item.proprietario.email],
            fail_silently=False,
        )

    # Mostra la pagina di conferma
    return render(request, "confermaPrenotazione.html", {"item": item})
def apiLocation(request,id):
    try:
        sede=Sede.objects.get(id=id)
    except:
        return redirect("home")
    locations=Location.objects.filter(sede=sede)
    locations = json.dumps([{'id': loc.id.urn.replace('urn:uuid:',''), 'nome': loc.nome} for loc in locations])
    return render(request, 'api.html',{"locations":locations})

def apiScatole(request,id):
    print(id)
    try:
        sede=Sede.objects.get(id=id)
    except:
        return render(request, 'api.html',{"locations":[]})

    scatole=Scatola.objects.filter(location__sede=sede)
    print(scatole)
    scatole = json.dumps([{'id': loc.id.urn.replace('urn:uuid:',''), 'descrizione': loc.descrizione} for loc in scatole])
    return render(request, 'api.html',{"locations":scatole})


def iMieiOggetti(request):
    # Prende tutti gli oggetti di cui l'utente loggato è proprietario
    oggetti = Oggetto.objects.filter(proprietario=request.user)
    context = {
        'oggetti': oggetti,
    }
    return render(request, 'iMieiOggetti.html', context)

def apiSaveItem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
