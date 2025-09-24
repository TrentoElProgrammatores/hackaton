# forms.py
from django import forms
from .models import Oggetto, Location, Scatola  # importa i modelli corretti

class UploadItemForm(forms.ModelForm):
    # Sovrascrivo i campi per poter controllare widget / required / choices in modo chiaro
    titolo = forms.CharField(
        label='Titolo',
        widget=forms.TextInput(attrs={
            'placeholder': 'Titolo oggetto',
            'class': 'input pl-10',
            'id': 'titolo'
        })
    )

    descrizione = forms.CharField(
        label='Descrizione',
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Descrizione (opzionale)',
            'class': 'input pl-10',
            'id': 'descrizione',
            'rows': 4,
        })
    )

    # Evitiamo query al livello del modulo: inizializziamo con none() e popoleremo in __init__
    location = forms.ModelChoiceField(
        queryset=Location.objects.none(),
        empty_label='Seleziona una location',
        widget=forms.Select(attrs={
            'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200',
            'required': True,
        })
    )

    scatola = forms.ModelChoiceField(
        queryset=Scatola.objects.none(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200',
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
            'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200',
            'required': True,
        })
    )

    immagine = forms.ImageField(
        label='Immagine',
        required=False,
        widget=forms.FileInput(attrs={
            'id': 'profilePhoto',
            'accept': 'image/*',
            'class': 'sr-only',
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
                #self.fields['scatola'].queryset = Scatola.objects.filter(owner=self.user)
            except Exception:
                # fallback generico
                self.fields['scatola'].queryset = Scatola.objects.all()
            # esempio di help_text che hai voluto mostrare
            self.fields['titolo'].help_text = f"Form creato da {self.user.username}"
        else:
            self.fields['scatola'].queryset = Scatola.objects.none()

    class Meta:
        model = Oggetto
        fields = ('titolo', 'descrizione', 'location', 'scatola', 'dimensione', 'immagine')
