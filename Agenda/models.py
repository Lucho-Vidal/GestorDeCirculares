from django.db import models

# Create your models here.
class Agenda(models.Model):
    email= models.CharField(max_length=100, default='')
    apellidoYNombre= models.CharField(max_length=100, default='')
    subGerencia = models.CharField(max_length=100, default='',blank=True)
    telefono = models.CharField(max_length=50, default='',blank=True)
    celular = models.CharField(max_length=50, default='',blank=True)
    interno = models.CharField(max_length=20, default='',blank=True)

    def __str__(self):
        return self.apellidoYNombre + " de la subgerencia de: " + self.subGerencia