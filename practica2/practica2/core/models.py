from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from random import *


# Create your models here.
class Profile(models.Model):
    PROFESION_OPTIONS = (
        ('1', 'Matemático'),
        ('2', 'Físico'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cui = models.IntegerField(blank=False)
    profesion = models.CharField(max_length=1, choices=PROFESION_OPTIONS, blank=False  )

#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if not created:
        instance.profile.save()

def user_directory_path(instance, filename):
    return '{0}/{1}_{2}'.format(instance.user.username, randint(100000, 999999), filename)

class Archivo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, blank=True)
    archivo = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Retrato(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, blank=True)
    imagen = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

def random_string():
    return str(randint(1000000000, 9999999999))

class ConfirmacionRegistro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=10, blank=False, default=random_string)
    validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

