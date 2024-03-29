# Generated by Django 2.2 on 2019-04-15 00:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import practica2.core.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0008_archivo_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Retrato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=255)),
                ('imagen', models.FileField(upload_to=practica2.core.models.user_directory_path)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
