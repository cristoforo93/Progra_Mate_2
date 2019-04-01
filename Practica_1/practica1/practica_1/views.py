from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .forms import RegistroForm, RegistroExtra, AccesoForm, UpdateUser, UpdateExtra, DocumentForm
from django.contrib.auth import login, authenticate, logout
from django.db import transaction
from django.contrib.auth.models import User
from .models import Profile,Document
from django.contrib.auth.decorators import login_required

# Create your views here.


def inicio(request):
    context = {'titulo':'Inicio'}
    template = loader.get_template('base.html')
    return HttpResponse(template.render(context,request))


@transaction.atomic
def registro(request):
    if request.method == 'POST':
        user_form = RegistroForm(request.POST)
        extra_form = RegistroExtra(request.POST)
        if user_form.is_valid() and extra_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            extra_form = RegistroExtra(request.POST, instance = user.profile)
            extra_form.full_clean()
            extra_form.save()
            return HttpResponseRedirect(reverse('inicio'))
    else:
        user_form = RegistroForm()
        extra_form = RegistroExtra()

    return render(request, 'registro.html',{'formulario1':user_form,'formulario2':extra_form,'titulo':"Registro"})

def acceso(request):
    if request.method == 'POST':
        form = AccesoForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            nombre_usuario = data.get("nombre")
            contrasena = data.get("contra")
            acceso = authenticate(username=nombre_usuario,password=contrasena)
            if acceso is not None:
                login(request,acceso)
                return HttpResponseRedirect(reverse('usuario',kwargs={'user':nombre_usuario}))
            else:
                return HttpResponseRedirect(reverse('inicio'))
    else:
        form = AccesoForm()    
    
    return render(request, 'login.html', {'formulario':form,'titulo':"Acceso"})

def usuario(request, user):
    estudiante = User.objects.get(username=user)
    context = {
        'nombre': estudiante.first_name,
        'apellido': estudiante.last_name,
        'carnet': estudiante.profile.carne,
        'cui': estudiante.profile.cui,
        'profesion': estudiante.profile.profesion,
        'titulo': user
    }
    template = loader.get_template('usuario.html')
    return HttpResponse(template.render(context,request))

@login_required(login_url='/acceso/')
@transaction.atomic
def update_profile(request):

    username = None
    if request.user.is_authenticated:
        username = request.user.username


    if request.method == 'POST':
        user_form = UpdateUser(request.POST, instance=request.user)
        profile_form = UpdateExtra(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('usuario',kwargs={'user':username}))
    else:
        user_form = UpdateUser(instance=request.user)
        profile_form = UpdateExtra(instance=request.user.profile)

    return render(request, 'actualizar.html',{'formulario1':user_form,'formulario2':profile_form,'titulo':"Actualizar"})


def upload_files(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('inicio'))
    else:
        form = DocumentForm()

    
    return render(request, 'upload.html',{'form':form})
