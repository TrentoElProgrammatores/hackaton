# forms.py
from django import forms
from .models import Oggetto, Location, Scatola, Sede  # importa i modelli corretti
from django.contrib.auth.forms import AuthenticationForm

class UploadItemForm(forms.ModelForm):
    # Sovrascrivo i campi per poter controllare widget / required / choices in modo chiaro
    titolo = forms.CharField(
        label='Titolo',
        widget=forms.TextInput(attrs={
            'placeholder': 'Titolo oggetto',
            'class': 'form-control',
            'id': 'titolo'
        })
    )

    descrizione = forms.CharField(
        label='Descrizione',
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Descrizione (opzionale)',
            'class': 'form-control',
            'id': 'descrizione',
            'rows': 4,
        })
    )

    # Evitiamo query al livello del modulo: inizializziamo con none() e popoleremo in __init__
    location = forms.ModelChoiceField(
        queryset=Location.objects.none(),
        empty_label='Seleziona una location',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True,
        })
    )

    scatola = forms.ModelChoiceField(
        queryset=Scatola.objects.none(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    DIM_CHOICES = [
        ('piccolo', 'Piccolo'),
        ('medio', 'Medio'),
        ('grande', 'Grande'),
    ]
    dimensione = forms.ChoiceField(
        choices=DIM_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True,
        })
    )

    immagine = forms.ImageField(
        label='Immagine',
        required=False,
        widget=forms.FileInput(attrs={
            'id': 'profilePhoto',
            'accept': 'image/*',
            'class': 'form-control',
        })
    )

    def __init__(self, *args, **kwargs):
        # recupero lo user dai kwargs (passalo dalla view)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # popolo i queryset qui per evitare query a import time


        # esempio: se vuoi mostrare solo le "scatole" dell'utente (se esiste un campo owner)
        if self.user is not None:
            print("User", self.user)
            try:
                self.fields['location'].queryset = Location.objects.filter(sede=self.user)
                self.fields['scatola'].queryset = Scatola.objects.filter(location__sede=self.user)
            except Exception:
                # fallback generico
                self.fields['location'].queryset = Location.objects.none()
                self.fields['scatola'].queryset = Scatola.objects.none()
            # esempio di help_text che hai voluto mostrare
            self.fields['titolo'].help_text = f"Form creato da {self.user.username}"
        else:
            self.fields['scatola'].queryset = Scatola.objects.none()

    class Meta:
        model = Oggetto
        fields = ('titolo', 'descrizione', 'location', 'scatola', 'dimensione', 'immagine')



class UploadScatolaForm(forms.ModelForm):
    descrizione = forms.CharField(
        label='Descrizione',
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Descrizione (opzionale)',
            'class': 'form-control',
            'rows': 4,
        })
    )

    location = forms.ModelChoiceField(
        queryset=Location.objects.none(),
        empty_label='Seleziona una location',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Scatola
        fields = ['descrizione', 'location']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filtra le location disponibili per l'utente
            user_locations = Location.objects.filter(sede=user)
            self.fields['location'].queryset = user_locations


class UploadLocationForm(forms.ModelForm):
    nome = forms.CharField(
        label="Nome",
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome della location',
            'class': 'form-control',
            'id': 'nome'
        })
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # l'utente loggato
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.sede = self.user  # assegna automaticamente la sede
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Location
        fields = ('nome',)

class SedeLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
