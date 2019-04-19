from django.core.mail import send_mail
from django.conf import settings
from practica2.core.models import ConfirmacionRegistro
from django.utils import timezone

class Email:

    def send_confirmation_email(self, user,host):
        # Enviar correo con enlace de confirmacion
        confirmacion = ConfirmacionRegistro(user_id=user.id)
        confirmacion.save()
        subject = 'Confirmación de registro'
        message = 'Hola, gracias por registrarte. Seguir el siguiente link para completar el registro: \n http://{0}/registro/confirmar/{1}'.format(host,confirmacion.token) 
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email,]
        send_mail( subject, message, email_from, recipient_list )
        print ('Email enviado:')
        print (message)

    def send_login_mail(self, request):
        subject = 'Alerta de acceso'
        message = 'El usuario {0} acaba de accesar a la plataforma con los siguientes datos:\n\n\tFecha y hora: {1}\n\n\tIp del login: {2}'.format(request.user.username,timezone.now(), request.META.get('REMOTE_ADDR') ) 
        email_from = settings.EMAIL_HOST_USER
        print(request.user.email)
        recipient_list = [request.user.email,]
        send_mail( subject, message, email_from, recipient_list )
        print ('Email enviado:')
        print (message)
        #Fecha y hora del login
        #Ip del login
        return ''


from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    Email().send_login_mail(request)
