from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect
from django.core.mail import send_mail
from .forms import *
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv
from urllib.parse import quote, urlencode, unquote

def sendEmail(text, to,azione):
    with open('log_email.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([text, to, azione])

# Create your views here.
def home(request):
    print(unquote("pbkdf2_sha256%241000000%247kSPqGEGH2VJx6cI1Pah3t%24oBUcLtXJmZ%2BE31BviEqUFndrzkejfTCqw8YeyIZfays%3D").replace("PASS","/"))
    #print(DocumentiCliente.objects.get(utente=request.user))
    if request.user.is_authenticated:
        items=Oggetto.objects.all().exclude(location__sede=request.user)
        return render(request, 'home.html',{"items":items})
    else:
        return render(request, 'home.html',{"items":Oggetto.objects.all()})

def addItem(request):
    if request.user.is_anonymous:
        return redirect('home')
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
    except:
        return redirect("home")
    data={'item':item}
    categoria=OggettoCategoria.objects.filter(oggetto=item).first()
    data.update({'categoria':categoria})
    scambio=MerceScambiata.objects.filter(oggetto=item)
    data.update({'scambi':scambio.order_by('-scambio__createdAt'),'domain':settings.DOMINIO})
    return render(request, 'prodotto.html',data)

def addScatola(request):
    if request.user.is_anonymous:
        return redirect('home')
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
    if request.user.is_anonymous:
        return redirect('home')
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
        form = SedeLoginForm()

    return render(request, 'sedeLogin.html', {'form': form})

def sedeLogout(request):
    """
    View per fare il logout dell'utente.
    """
    logout(request)  # termina la sessione dell'utente
    return redirect('sedeLogin')  # reindirizza alla pagina di login


def editProduct(request,id):
    if request.user.is_anonymous:
        return redirect('home')
    if request.user.is_anonymous:
        return redirect('home')
    sedi=Sede.objects.all().exclude(username=request.user.username)
    try:
        prodotto=Oggetto.objects.get(id=id)
    except:
        return redirect("home")
    return render(request, 'editProduct.html',{'sedi':sedi,'item':prodotto})



def confermaPrenotazione(request, item_id):
    if request.user.is_anonymous:
        return redirect('home')
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
        sede=Sede.objects.get(username=id)
    except:
        print(id,'idsede')
        return redirect("home")
    print("DIOCANE")
    locations=Location.objects.filter(sede=sede)
    locations = json.dumps([{'id': loc.id.urn.replace('urn:uuid:',''), 'nome': loc.nome} for loc in locations])
    return render(request, 'api.html',{"locations":locations})

def apiScatole(request,id):
    try:
        sede=Sede.objects.get(username=id)
    except:
        return render(request, 'api.html',{"locations":[]})

    scatole=Scatola.objects.filter(location__sede=sede)
    print(scatole)
    scatole = json.dumps([{'id': loc.id.urn.replace('urn:uuid:',''), 'descrizione': loc.descrizione} for loc in scatole])
    return render(request, 'api.html',{"locations":scatole})


def iMieiOggetti(request):
    if request.user.is_anonymous:
        return redirect('home')

    # Prende il parametro di ricerca dalla query string
    search_query = request.GET.get("q", "")

    # Prende tutti gli oggetti dell'utente
    oggetti = Oggetto.objects.filter(proprietario=request.user)

    # Se è stato inserito un termine di ricerca, filtra
    if search_query:
        oggetti = oggetti.filter(titolo__icontains=search_query)

    context = {
        "oggetti": oggetti,
        "search_query": search_query,  # 👉 da usare nel template per mantenere il valore nel campo
    }
    return render(request, "iMieiOggetti.html", context)


@csrf_exempt
def apiSaveItem(request):
    if request.user.is_anonymous:
        return redirect('home')
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)

        item=Oggetto.objects.get(id=data['id'])
        da=item.location
        item.scatola=Scatola.objects.get(id=data['scatola'])
        item.location=Location.objects.get(id=data['location'])
        item.save()
        item.location.sede=Sede.objects.get(username=data['sede'])
        item.location.save()
        a=item.location
        MerceScambiata.objects.create(oggetto=item,scambio=Scambi.objects.create(da=da,a=a)).save()
        return JsonResponse({'success': True}, status=200)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


def leMieScatole(request):
    if request.user.is_anonymous:
        return redirect('home')

    #Recupera tutte le location dell'utente loggato
    locations = Location.objects.filter(sede=request.user)

    #Prende i parametri GET
    location_id = request.GET.get("location")
    search_query = request.GET.get("q")  # nuovo campo per la ricerca per descrizione

    # Query base: tutte le scatole dell'utente
    scatole = Scatola.objects.filter(location__sede=request.user).order_by("-createdAt")
    
    # Filtro per location
    if location_id:
        scatole = scatole.filter(location_id=location_id)

    # Filtro per descrizione (ricerca parziale, case-insensitive)
    if search_query:
        scatole = scatole.filter(descrizione__icontains=search_query)

    context = {
        "scatole": scatole,
        "locations": locations,
        "selected_location": location_id,
        "search_query": search_query,  # 👈 da usare nel template
    }

    return render(request, "leMieScatole.html", context)




# views.py
def oggettiInScatola(request, scatola_id):
    if request.user.is_anonymous:
        return redirect('home')
    # prendi la scatola dell'utente loggato
    scatola = Scatola.objects.get(id=scatola_id)#get_object_or_404(Scatola, id=scatola_id, location__sede=request.user)

    # prendi tutti gli oggetti collegati a questa scatola
    oggetti = Oggetto.objects.filter(scatola=scatola) # relazione inversa FK

    return render(request, "oggettiInScatola.html", {"scatola": scatola, "oggetti": oggetti})


def aggiungi_oggetto_view(request, scatola_id):
    if request.user.is_anonymous:
        return redirect('home')
    scatola = get_object_or_404(Scatola, id=scatola_id)

    # Oggetti disponibili (non ancora in nessuna scatola)
    oggetti_disponibili = Oggetto.objects.filter(scatola__isnull=True)

    context = {
        'scatola': scatola,
        'oggetti': oggetti_disponibili,
    }
    return render(request, 'aggiungi_oggetto.html', context)


def aggiungi_oggetto_scatola(request, scatola_id, oggetto_id):
    if request.user.is_anonymous:
        return redirect('home')
    scatola = get_object_or_404(Scatola, id=scatola_id)
    oggetto = get_object_or_404(Oggetto, id=oggetto_id)

    # Associa l'oggetto alla scatola (assumendo ForeignKey da Oggetto a Scatola)
    oggetto.scatola = scatola
    oggetto.save()

    return redirect('aggiungi_oggetto', scatola_id=scatola.id)


def rimuovi_dalla_scatola(request, oggetto_id):
    if request.user.is_anonymous:
        return redirect('home')
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

def recupero_password(request):
    if request.user.is_anonymous:
        return redirect('home')

    if request.method == 'POST':
        form = PasswordLostForm(data=request.POST)
        if form.is_valid():
            # Recupera l'utente autenticato

            request.user.set_password(form.cleaned_data['password'])
            request.user.save()

            return redirect('home')  # Sostituisci con il nome della tua dashboard
        print(form.errors)
    else:
        form = PasswordLostForm()
    return render(request, 'password_reset.html', {'form': form})
'''
def verifica_recupero(request,id):
    try:
        sede=Sede.objects.get(password=unquote(id).replace("PASS",'/'))
    except:
        return render(request, 'verifica_recupero.html',{'validate':False})
    print("sede",sede)
    sede.set_password(Password.objects.get(dioHash=unquote(id).replace("PASS",'/')).password)
    sede.save()
    print("GODO")
    return render(request, 'verifica_recupero.html',{'validate':True})'''


def elimina_oggetto(request, pk):
    if request.method == "POST":
        oggetto = get_object_or_404(Oggetto, pk=pk, proprietario=request.user)
        oggetto.delete()
        messages.success(request, "Oggetto eliminato con successo!")
        return redirect("iMieiOggetti")  # oppure la pagina che vuoi dopo l'eliminazione
    return redirect("prodotto", pk=pk)


def elimina_scatola(request, scatola_id):
    if request.method == "POST":
        scatola = get_object_or_404(Scatola, id=scatola_id, location__sede=request.user)

        # Svuota la scatola: tutti gli oggetti collegati diventano senza scatola
        Oggetto.objects.filter(scatola=scatola).update(scatola=None)

        # Elimina la scatola
        scatola.delete()
        messages.success(request, "Scatola eliminata con successo!")
        return redirect("leMieScatole")

    return redirect("leMieScatole")