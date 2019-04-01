from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    profesiones = {
        ('Matemático','Matemático'),
        ('Físico','Físico')
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carne = models.CharField(max_length = 10, default = '')
    cui = models.CharField(max_length = 100, default = '')
    profesion = models.CharField(max_length = 100, choices = profesiones, default = '')

    def __str__(self):
        return self.user.username

class Document(models.Model):
    name_file = models.CharField(max_length=100, default='')
    document = models.FileField(upload_to='documents/')


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
       Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=User)
def save_user(sender, instance, **kwargs):
    instance.profile.save()