from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Document


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

class RegistroExtra(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'carne',
            'cui',
            'profesion'
        )

class AccesoForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        required=True,
        label="",
        widget=(forms.TextInput(attrs={"placeholder":"Nombre de Usuario","class":"input-login"}))
    )
    contra = forms.CharField(
        max_length=100,
        required=True,
        label="",
        widget=(forms.PasswordInput(attrs={"placeholder":"Contraseña","class":"input-login"}))
    )

class UpdateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email'
        )

class UpdateExtra(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'carne',
            'cui',
            'profesion'
        )

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name_file', 'document')