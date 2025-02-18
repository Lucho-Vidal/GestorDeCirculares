from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required  
from .models import Agenda
from .forms import AgendaForm

# Create your views here.
@login_required
def agenda(request):
    # circulares = Circular.objects.all()
    contactos = Agenda.objects.all()
    if request.method == 'GET':
        return render(request, "agenda.html",{
            'contactos': contactos,
            'titulo' : 'Contactos' 
        })

@login_required
def createContacto(request):
    if request.method == 'GET':
        return render(request, "createContacto.html",{
            'form': AgendaForm,
            'titulo':'Nuevo contacto',
        })
    else:
        try:
            form = AgendaForm(request.POST or None)
            nuevoContacto = form.save(commit=False)
            nuevoContacto.save()
            return redirect('agenda')
        except ValueError:
            print(ValueError)
            return render(request, "createContacto.html",{
                'form': AgendaForm,
                'titulo':'Nuevo contacto',
                'error': 'Por favor, ingrese datos validos'
            })
        
@login_required
def editContacto(request, id):
    contacto = get_object_or_404(Agenda, pk=id)  

    if request.method == 'GET':
        form = AgendaForm(instance=contacto)
        return render(request, "createContacto.html", {
            'form': form,
            'titulo': 'Editar contacto',
        })
    else:
        try:
            form = AgendaForm(request.POST, instance=contacto) 
            if form.is_valid():  
                form.save()
                return redirect('agenda')
            else:
                return render(request, "createContacto.html", {
                    'form': form,
                    'titulo': 'Editar contacto',
                    'error': 'Por favor, ingrese datos válidos'
                })
        except ValueError:
            return render(request, "createContacto.html", {
                'form': form,
                'titulo': 'Editar contacto',
                'error': 'Error al procesar el formulario'
            })
    
@login_required
def deleteContacto(request,id):
    agenda = get_object_or_404(Agenda,pk=id)
    if request.method == 'POST':
        agenda.delete()
        return redirect('agenda')
    return render(request, 'confirm_delete.html', {'agenda': agenda})
        