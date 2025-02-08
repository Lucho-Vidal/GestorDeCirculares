from django.contrib import admin
from .models import Circular

class CircularAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

# Register your models here.
admin.site.register(Circular)