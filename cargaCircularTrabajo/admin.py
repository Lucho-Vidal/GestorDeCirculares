from django.contrib import admin
from .models import Circular, Estacion

class CircularAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

class EstacionAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

# Register your models here.
admin.site.register(Circular)
admin.site.register(Estacion)