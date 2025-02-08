from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required  
from django.db import IntegrityError
from django.utils import timezone
from .forms import CircularForm
from .models import Circular

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
        return render(request, "createCircular.html",{
            'form': CircularForm
        })
    else:
        try:
            form = CircularForm(request.POST)
            new_circular = form.save(commit=False)
            new_circular.user = request.user
            new_circular.save()
            return redirect('circulares')
        except ValueError:
            return render(request, "createCircular.html",{
                'form': CircularForm,
                'error': 'Por favor, ingrese datos validos'
            })
    
@login_required
def circulares(request):
    # circulares = Circular.objects.all()
    circulares = Circular.objects.filter(user=request.user, datecompleted__isnull=True)
    if request.method == 'GET':
        return render(request, "circulares.html",{
            'circulares': circulares
        })
        
@login_required
def circularesCompleted(request):
    # circulares = Circular.objects.all()
    circulares = Circular.objects.filter(user=request.user, datecompleted__isnull=False)
    if request.method == 'GET':
        return render(request, "circulares.html",{
            'circulares': circulares
        })

@login_required
def circularDetalle(request,id):
    if request.method == 'GET':
        circular = get_object_or_404(Circular,pk=id, user=request.user)
        form = CircularForm(instance=circular)
        return render(request, "circularDetalle.html",{
            'circular': circular,
            'form': form
        })
    else:
        try:
            circular = get_object_or_404(Circular,pk=id, user=request.user)
            form = CircularForm(request.POST,instance=circular)
            form.save()
            return redirect('circulares')
        except ValueError:
            return render(request, "circulares.html",{
                'circulares': circulares,
                'error':"Error al actualizar la circular"
            })

@login_required
def completeCircular(request,id):
    circular = get_object_or_404(Circular,pk=id,user=request.user)
    if request.method == 'POST':
        circular.datecompleted = timezone.now()
        circular.save()
        return redirect('circulares')
        
@login_required
def deleteCircular(request,id):
    circular = get_object_or_404(Circular,pk=id,user=request.user)
    if request.method == 'POST':
        circular.delete()
        return redirect('circulares')
        
