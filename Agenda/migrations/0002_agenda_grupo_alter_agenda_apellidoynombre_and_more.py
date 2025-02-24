# Generated by Django 5.1.6 on 2025-02-22 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agenda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenda',
            name='grupo',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='apellidoYNombre',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='celular',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='email',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='interno',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='subGerencia',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='telefono',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
