from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required  
from django.db import IntegrityError
from django.utils import timezone
from .forms import CircularForm
from .models import Agenda, Circular, Estacion
import json

# Create your views here.

def signIn(request):
    if request.method == "GET":
        return render(request, "signin.html", {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "signin.html", {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña es incorrecto'
            })
        else:
            login(request, user)
            return redirect('home')
        
def signUp(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "El usuario ya existe!"},
                )
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm,
             "error": "Las contraseñas no coinciden"},
        )

def signOut(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, "home.html")

@login_required
def createCircular(request):
    if request.method == 'GET':
        estaciones = Estacion.objects.all()
        contactos = Agenda.objects.all()
        contactos_json = json.dumps([{"id": c.id, "apellidoYNombre": c.apellidoYNombre} for c in contactos])
        return render(request, "createCircular.html",{
            'form': CircularForm,
            'estaciones': estaciones,
            'contactos_json': contactos_json,
            'contactos': contactos
        })
    else:
        try:
            form = CircularForm(request.POST)
            new_circular = form.save(commit=False)
            new_circular.user = request.user
            new_circular.save()
            new_circular.responsable.set(request.POST.getlist('responsable'))
            return redirect('circulares')
        except ValueError:
            return render(request, "createCircular.html",{
                'form': CircularForm,
                'error': 'Por favor, ingrese datos validos'
            })
    
@login_required
def circulares(request):
    # circulares = Circular.objects.all()
    circulares = Circular.objects.all()
    if request.method == 'GET':
        return render(request, "circulares.html",{
            'circulares': circulares,
            'titulo' : 'Circulares' 
        })
        
@login_required
def circularesCompleted(request):
    # circulares = Circular.objects.all()
    circulares = Circular.objects.filter(user=request.user, datecompleted__isnull=False)
    if request.method == 'GET':
        return render(request, "circulares.html",{
            'circulares': circulares,
            'titulo' : 'Circulares completadas' 
        })

@login_required
# def circularDetalle(request, id):
#     circular = get_object_or_404(Circular, pk=id, user=request.user)
#     estaciones = Estacion.objects.all()
#     contactos = Agenda.objects.all()
#     contactos_json = json.dumps([{"id": c.id, "apellidoYNombre": c.apellidoYNombre} for c in contactos])

#     if request.method == 'GET':
#         form = CircularForm(instance=circular)
#         return render(request, "circularDetalle.html", {
#             'circular': circular,
#             'form': form,
#             'estaciones': estaciones,
#             'contactos': contactos,
#             'contactos_json': contactos_json,
#         })
#     else:
#         try:
#             print(request.POST)
#             print('--------------------')
#             print("Responsable IDs:", request.POST.getlist('responsable'))

#             form = CircularForm(request.POST, instance=circular)
#             if form.is_valid():
#                 circular = form.save(commit=False)  # Guardar sin confirmar en la BD aún
#                 responsable_ids = request.POST.getlist('responsable')  # Obtener lista de IDs
#                 responsables = Agenda.objects.filter(id__in=responsable_ids)  # Filtrar por IDs
#                 circular.save()  # Guardar la circular primero (necesario para la relación M2M)
#                 circular.responsable.set(responsables)  # Asignar los responsables correctamente
#                 circular.save()
#                 print("Responsables guardados:", circular.responsable.all())
#                 return redirect('circulares')
#         except ValidationError:
#             return render(request, "circularDetalle.html", {
#                 'circular': circular,
#                 'form': form,
#                 'error': "Error al actualizar la circular"
#             })
def circularDetalle(request, id):
    circular = get_object_or_404(Circular, pk=id, user=request.user)
    estaciones = Estacion.objects.all()
    contactos = Agenda.objects.all()
    contactos_json = json.dumps([{"id": c.id, "apellidoYNombre": c.apellidoYNombre} for c in contactos])

    if request.method == 'GET':
        form = CircularForm(instance=circular)
        return render(request, "circularDetalle.html", {
            'circular': circular,
            'form': form,
            'estaciones': estaciones,
            'contactos': contactos,
            'contactos_json': contactos_json,
        })

    # elif request.method == 'POST':
    else:
        try:
            print(request.POST)  # ✅ Depuración
            form = CircularForm(request.POST, instance=circular)

            if form.is_valid():
                circular = form.save(commit=False)  

                responsable_ids = [r for r in request.POST.getlist('responsable') if r ]  # Filtrar valores vacíos
                responsables = Agenda.objects.filter(id__in=responsable_ids)  # Filtrar solo responsables válidos
                circular.save()  # ✅ Guardar primero antes de asignar M2M
                circular.responsable.set(responsables)  # ✅ Asignar correctamente
                circular.save()  # ✅ Guardar M2M

                return redirect('circulares')  # ✅ Redirigir después de éxito
            
            else:
                print("Formulario inválido:", form.errors)  # ✅ Depuración de errores

        except ValidationError:
            return render(request, "circularDetalle.html", {
                'circular': circular,
                'form': form,
                'error': "Error al actualizar la circular",
                'estaciones': estaciones,
                'contactos': contactos,
                'contactos_json': contactos_json,
            })
    
    print(request.method)
    # 🔴 IMPORTANTE: Si no es un GET ni un POST, debe devolver un HttpResponse.
    return render(request, "circularDetalle.html", {
        'circular': circular,
        'form': CircularForm(instance=circular),
        'estaciones': estaciones,
        'contactos': contactos,
        'contactos_json': contactos_json,
        'error': "Método HTTP no permitido",
    })


@login_required
def completeCircular(request,id):
    circular = get_object_or_404(Circular,pk=id,user=request.user)
    if request.method == 'POST':
        print(circular)
        if circular.datecompleted:
            print('ingreso')
            circular.datecompleted = timezone.now()
        else:
            circular.datecompleted = None
        circular.save()
        return redirect('circulares')
        
@login_required
def deleteCircular(request,id):
    circular = get_object_or_404(Circular,pk=id,user=request.user)
    if request.method == 'POST':
        circular.delete()
        return redirect('circulares')
        
