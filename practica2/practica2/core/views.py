from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage 
from django import forms
from os.path import splitext
from practica2.core.models import Profile,Archivo,Retrato,ConfirmacionRegistro
from practica2.core.forms import UserForm,ProfileForm, ArchivoForm, RetratoForm
from practica2.automata import analizar_texto
from practica2.email import Email
from django.utils import timezone
import datetime


# Create your views here.
def home(request):
    count = User.objects.count()
    return render(request, 'home.html', {
        'count': count
    })

@login_required
def post_login_redirect(request):
    return redirect('profile',username=request.user.username)

@transaction.atomic
def registro(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.profile = Profile(user_id=user.id, cui=request.POST.get("cui",""), profesion=request.POST.get("profesion",""))
            user.is_active = False
            user.save()
            Email().send_confirmation_email(user,request.META['HTTP_HOST'])
            return redirect('home')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'registration/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'form_type_signin': True
    })


@login_required
def change_admin(request):
    print("change admin")
    user = request.user
    user.is_superuser = not user.is_superuser
    user.save()
    return redirect('post_login_redirect')

def confirmar_registro(request,token):
    confirmacion = ConfirmacionRegistro.objects.filter(token=token).first()
    if confirmacion and not confirmacion.validated :
        if confirmacion.created_at + datetime.timedelta(minutes=10) >= timezone.now():
            confirmacion.user.is_active = True 
            confirmacion.user.save()
            confirmacion.validated = True
            confirmacion.save()
            return render(request,'confirmar_registro.html', {
                'message': 'Confirmacion de correo exitosa. Ya puedes pasar al login.'
            })
        else:
            Email().send_confirmation_email(confirmacion.user,request.META['HTTP_HOST'])
            return render(request,'confirmar_registro.html', {
                'message': 'Token expirado. Se te ha enviado un nuevo token a tu correo.'
            })
    else:

        return render(request,'confirmar_registro.html', {
            'message': 'Error: Token ya utilizado o inexistente.'
        })

    return render(request,'confirmar_registro.html', {
        'message': 'Error inesperado.'
    })


@login_required
def profile(request, username):
    if username == request.user.username :
    #u = User.objects.get(username=username)
        return render(request,'profile.html')
    else:
        return render(request,'error.html', {
            'message': 'La pagina que buscas no existe.'
        })


@transaction.atomic
@login_required
def editar_perfil(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        #if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        user.profile = profile_form.save()
        return redirect('post_login_redirect')
    else:
        user_form = UserForm({
            'username': request.user.username,
            'email': request.user.email
        })
        profile_form = ProfileForm( {
            'cui': request.user.profile.cui,
            'profesion': request.user.profile.profesion
        })
    return render(request, 'registration/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'form_type_edit': True
    })


@login_required
def archivos(request):
    archivos = Archivo.objects.filter(user_id=request.user.id)
    archivos_otros = Archivo.objects.all().exclude(user_id=request.user.id)
    return render(request, 'archivos/index.html', {
        'archivos': archivos,
        'archivos_otros': archivos_otros,
    })

@login_required
def nuevo_archivo(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES, instance=Archivo(user_id=request.user.id))
        filearchivo = request.FILES['archivo']
        ext = splitext(filearchivo.name)[1]
        ext = ext.lower()
        if ext != '.p2':
            msg = "El tipo de archivo no es .p2. Archivo subido: " + ext
            form.add_error('archivo',msg)
        if form.is_valid():
            form.save()
            return redirect('archivos')
    else:
        form = ArchivoForm()
    return render(request, 'archivos/new.html', {
        'form': form
    })

@login_required
def eliminar_archivo(request,id):
    archivo = Archivo.objects.get(id=id)
    archivo.delete()
    return redirect('archivos')

@login_required
def editar_archivo(request,id):

    archivo = Archivo.objects.get(id=id)
    if request.method == 'POST':
        with open(archivo.archivo.path, 'r+') as my_file:
            print("contenido del post:")
            print(request.POST.get("contenido",""))
            print(archivo.archivo.path)
            
            my_file.seek(0)
            my_file.write(request.POST.get("contenido",""))
            my_file.truncate()
            #fs = FileSystemStorage()
            #filearchivo = fs.open(str(archivo.archivo),'w')
            #archivo.archivo.save(str(archivo.archivo),request.POST.get("contenido",""),save=True)
        return redirect('analizar_archivo',archivo.id)

    fs = FileSystemStorage()
    file_lines = fs.open(str(archivo.archivo),'r').readlines()
    #fs.close()
    contenido = ''
    for line in file_lines:
        contenido += line
    return render(request, 'archivos/editar.html', {
        'contenido': contenido,
        'archivo': archivo,
    })

@login_required
def analizar_archivo(request,id):
    archivo = Archivo.objects.get(id=id)
    fs = FileSystemStorage()
    file_lines = fs.open(str(archivo.archivo),'r').readlines()
    #fs.close()
    contenido = ''

    for line in file_lines:
        contenido += line #+ '\n'

    analizador = analizar_texto()
    analizador.analizar(contenido)

    return render(request, 'archivos/analisis.html', {
        'contenido': analizador.colorear_html(contenido),
        'original': contenido.replace('\n','<br/>'),
        'archivo': archivo,
        'log': analizador.get_log()
    })

@login_required
def retratos(request):
    retratos = Retrato.objects.filter(user_id=request.user.id)
    retratos_otros = Retrato.objects.all().exclude(user_id=request.user.id)
    return render(request, 'retratos/index.html', {
        'retratos': retratos,
        'retratos_otros': retratos_otros,
    })

@login_required
def nuevo_retrato(request):
    if request.method == 'POST':
        form = RetratoForm(request.POST, request.FILES, instance=Retrato(user_id=request.user.id))
        fileretrato = request.FILES['imagen']
        if form.is_valid():
            form.save()
            return redirect('retratos')
    else:
        form = RetratoForm()
    return render(request, 'retratos/new.html', {
        'form': form
    })

@login_required
def eliminar_retrato(request,id):
    retrato = Retrato.objects.get(id=id)
    retrato.delete()
    return redirect('retratos')

