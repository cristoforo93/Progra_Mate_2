from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from practica2.core.models import Profile, Archivo, Retrato

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'cui',
            'profesion',
        )
        labels = {
            'cui': 'CUI',
            'profesion': 'Profesión',
        }


class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = (
            'nombre',
            'archivo',
        )
        labels = {
            'nombre': 'Nombre',
            'archivo': 'Archivo',
        }

class RetratoForm(forms.ModelForm):
    class Meta:
        model = Retrato
        fields = (
            'nombre',
            'imagen',
        )
        labels = {
            'nombre': 'Nombre',
            'imagen': 'Imagen',
        }