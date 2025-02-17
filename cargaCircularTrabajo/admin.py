from django.contrib import admin
from .models import Circular, Agenda, Estacion

class CircularAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)
class AgendaAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)
class EstacionAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

# Register your models here.
admin.site.register(Circular)
admin.site.register(Agenda)
admin.site.register(Estacion)