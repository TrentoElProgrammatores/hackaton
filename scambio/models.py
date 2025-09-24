from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.



class Categoria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=200)


class Sede(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=200)
    indirizzo=models.CharField(max_length=200)

    def __str__(self):
        return self.username

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sede = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome=models.CharField(max_length=200, default="Campeione 1")

    def __str__(self):
        return self.nome

class Scatola(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    descrizione = models.TextField()

    # WARN: La location della scatola ha la priorità
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.location.nome

class Oggetto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titolo = models.CharField(max_length=200)
    descrizione = models.TextField()
    proprietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scatola = models.ForeignKey(Scatola, on_delete=models.CASCADE)

    # WARN: La location della scatola ha la priorità
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)

    dimensione = models.CharField(max_length=200,choices=[(0,'piccolo'),(1,'medio'),(2,'grande')], blank=True, null=True),
    immagine=models.ImageField(upload_to='oggetti/', blank=True, null=True)


    def __str__(self):
        return self.titolo
    
class OggettoCategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    oggetto = models.ForeignKey(Oggetto, on_delete=models.CASCADE)

class MerceScambiata(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    oggetto=models.ForeignKey(Oggetto, on_delete=models.CASCADE, blank=True, null=True)
    scatola=models.ForeignKey(Scatola, on_delete=models.CASCADE, blank=True, null=True)

class Scambi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merceScambiata=models.ForeignKey(MerceScambiata, on_delete=models.CASCADE)
    createdAt=models.DateTimeField(default=timezone.now, null=True, blank=True) 
    da=models.ForeignKey(Location, on_delete=models.CASCADE, related_name="mittente_scambio")
    a=models.ForeignKey(Location, on_delete=models.CASCADE, related_name="destinatario_scambio")


class Noleggio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdAt=models.DateTimeField(default=timezone.now, null=True, blank=True) 
    da=models.ForeignKey(Location, on_delete=models.CASCADE, related_name="mittente_noleggio")
    a=models.CharField(max_length=200)
    ritorno=models.DateTimeField(default=timezone.now, null=True, blank=True) 



