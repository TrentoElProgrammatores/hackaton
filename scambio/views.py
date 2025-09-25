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
from django.views.decorators.csrf import csrf_exempt

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
        if form.is_valid():
            # Salva la scatola
            scatola = form.save(commit=False)
            scatola.save()

            # Recupera gli oggetti selezionati e assegna la scatola
            oggetti_selezionati = form.cleaned_data.get('oggetti')
            if oggetti_selezionati:
                for oggetto in oggetti_selezionati:
                    oggetto.scatola = scatola
                    oggetto.save()

            # Reindirizza alla lista delle scatole
            return redirect('leMieScatole')
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
    sedi=Sede.objects.all()
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

@csrf_exempt  
def apiSaveItem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        item=Oggetto.objects.get(id=data['id'])
        item.scatola=Scatola.objects.get(id=data['scatola'])
        item.location=Location.objects.get(id=data['location'])
        item.save()
        return JsonResponse({'success': True}, status=200)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


def leMieScatole(request):
    scatole = Scatola.objects.filter(location__sede=request.user).order_by("-createdAt")
    return render(request, "leMieScatole.html", {"scatole": scatole})


# views.py
def oggettiInScatola(request, scatola_id):
    # prendi la scatola dell'utente loggato
    scatola = Scatola.objects.get(id=scatola_id)#get_object_or_404(Scatola, id=scatola_id, location__sede=request.user)

    # prendi tutti gli oggetti collegati a questa scatola
    oggetti = Oggetto.objects.filter(scatola=scatola) # relazione inversa FK

    return render(request, "oggettiInScatola.html", {"scatola": scatola, "oggetti": oggetti})


def aggiungi_oggetto_view(request, scatola_id):
    scatola = get_object_or_404(Scatola, id=scatola_id)

    # Oggetti disponibili (non ancora in nessuna scatola)
    oggetti_disponibili = Oggetto.objects.filter(scatola__isnull=True)

    context = {
        'scatola': scatola,
        'oggetti': oggetti_disponibili,
    }
    return render(request, 'aggiungi_oggetto.html', context)


def aggiungi_oggetto_scatola(request, scatola_id, oggetto_id):
    scatola = get_object_or_404(Scatola, id=scatola_id)
    oggetto = get_object_or_404(Oggetto, id=oggetto_id)

    # Associa l'oggetto alla scatola (assumendo ForeignKey da Oggetto a Scatola)
    oggetto.scatola = scatola
    oggetto.save()

    return redirect('aggiungi_oggetto', scatola_id=scatola.id)


def rimuovi_dalla_scatola(request, oggetto_id):
    oggetto = get_object_or_404(Oggetto, id=oggetto_id)

    # Salva l'ID della scatola corrente prima di rimuovere
    scatola_id = oggetto.scatola.id if oggetto.scatola else None

    # Rimuovi l'oggetto dalla scatola
    oggetto.scatola = None
    oggetto.save()

    # Reindirizza solo se c'era una scatola
    if scatola_id:
        return redirect('oggettiInScatola', scatola_id=scatola_id)
    else:
        return redirect('home')  # o un'altra pagina a tua scelta

