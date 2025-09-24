from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.conf import settings


class UploadItemForm(forms.ModelForm):
    class Meta:
        model = Oggetto
        fields = ('titolo','descrizione','location', 'scatola', 'dimensione', 'immagine') # Includi i tuoi campi personalizzati
        widgets = {
            'titolo':forms.CharField(
                label='Full Name',
                widget=forms.TextInput(attrs={
                    'placeholder': 'John Doe',
                    'class': 'input pl-10',
                    'id': 'name'
                })
            ),
            
            'descrizione':forms.Select(choices=[cat for cat in settings.PROV_ITALIA.keys()], attrs={
                'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200',
                'required': True,
            }),

            'location':forms.Select(choices=[provincia for province_list in settings.PROV_ITALIA.values() for provincia in province_list], attrs={
                'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200',
                'required': True,
            }),
            'scatola':forms.Select(choices=[], attrs={
                'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200',
                'required': True,
            }),

            'dimensione':forms.Select(choices=['piccolo','medio','grande'], attrs={
                'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200',
                'required': True,
            }),
            'immagine':forms.Select(choices=[provincia for province_list in settings.PROV_ITALIA.values() for provincia in province_list], attrs={
                'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200',
                'required': True,
            }),
            
        }
        labels = {
            'stato': 'State',
            'regione': 'Region',
            'provincia':'Province',
        }
