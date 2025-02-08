from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Circular(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True,blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title + ' - by ' + self.user.username
    
class agenda(models.Model):
    email= models.CharField(max_length=100)
    apellidoYNombre= models.CharField(max_length=100)
    subGerencia = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)
    interno = models.CharField(max_length=20)
        