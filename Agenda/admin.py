from django.contrib import admin
from .models import Agenda
class AgendaAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)
# Register your models here.
admin.site.register(Agenda)
