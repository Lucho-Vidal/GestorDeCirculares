from django.db import models
from django.contrib.auth.models import User
from Agenda.models import Agenda

class Estacion(models.Model):
    estacion = models.CharField(max_length=50)

    def __str__(self):
        return self.estacion
    

# Create your models here.
class Circular(models.Model):
    titulo = models.CharField(max_length=200,default='')
    created = models.DateTimeField(auto_now_add=True)
    Solicitante = models.CharField(max_length=200, default='-')
    fechaInicioTrabajo = models.DateTimeField()
    fechaFinTrabajo = models.DateTimeField()
    ocupaVia = models.BooleanField(default=False)
    necesitaCorteEnergia = models.BooleanField(default=False)
    
    # Sector
    kmInicio = models.CharField(max_length=10, default='-')
    PaloInicio = models.CharField(max_length=10, default='-')
    
    # Añadir related_name a evitar el conflicto
    estacionInicio = models.ForeignKey(Estacion, on_delete=models.SET_NULL, null=True, blank=True, related_name='circular_inicio_set')
    
    kmFin = models.CharField(max_length=10, default='-')
    paloFin = models.CharField(max_length=10, default='-')
    
    # Añadir related_name a evitar el conflicto
    estacionFin = models.ForeignKey(Estacion, on_delete=models.SET_NULL, null=True, blank=True, related_name='circular_fin_set')
    
    via = models.CharField(max_length=20, default='No ocupa')
    
    # Descripción
    descripcion = models.TextField(blank=True, default='-')
    responsable = models.ManyToManyField(Agenda, blank=True)
    
    # Se necesita presencia
    supervisorTransporte = models.BooleanField(default=False)
    piloto = models.BooleanField(default=False)
    personalPolicial = models.BooleanField(default=False)
    otro = models.BooleanField(default=False)
    detalleOtro = models.TextField(blank=True)
    
    # Creador 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + ' - by ' + self.user.username
