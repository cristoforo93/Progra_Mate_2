# Generated by Django 2.2 on 2019-04-12 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cui',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profesion',
            field=models.CharField(choices=[('1', 'Matemático'), ('2', 'Físico')], default=1, max_length=1),
        ),
    ]
