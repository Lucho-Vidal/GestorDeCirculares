from pathlib import Path
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required  
from django.contrib import messages
from django.db import IntegrityError
from django.utils import timezone
from .forms import CircularForm
from .models import Circular, Estacion
from Agenda.models import Agenda
import json
import fitz
import os
from textwrap import wrap
import win32com.client as win32
import pythoncom
from itertools import groupby

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
            responsable_ids = [r for r in request.POST.getlist('responsable') if r ]  # Filtrar valores vacíos
            responsables = Agenda.objects.filter(id__in=responsable_ids)  # Filtrar solo responsables válidos
            new_circular = form.save(commit=False)
            new_circular.user = request.user
            new_circular.save()
            new_circular.responsable.set(responsables)
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
    circular = get_object_or_404(Circular,pk=id)
    if request.method == 'POST':
        circular.delete()
        return redirect('circulares')
    return render(request, 'confirm_delete_circular.html', {'circular': circular})

def generar_pdf(circular):
    """
    Genera un PDF basado en la información de la circular y devuelve la ruta del archivo generado.
    """
    path_base = Path(__file__).resolve().parent.parent
    pdf_base = f"{path_base}/cargaCircularTrabajo/static/pdf/base.pdf"
    output_pdf = f"{path_base}/cargaCircularTrabajo/static/pdf/{circular.titulo}.pdf"

    # Si no existe la base, se crea un PDF vacío
    if not os.path.exists(pdf_base):
        doc = fitz.open()
        doc.insert_page(0, text="Gestor de Circulares")
        doc.save(pdf_base)
        doc.close()

    # Abrir el PDF base
    doc = fitz.open(pdf_base)
    page = doc[0]  # Primera página

    # Insertar logo en la parte superior
    rect = fitz.Rect(0, 30, 250, 80)  # Ajusta la posición según sea necesario
    page.insert_image(rect, filename=f"{path_base}/cargaCircularTrabajo/static/images/logo.png")

    y = 120  # Posición inicial en Y
    page.insert_text((250, y), f"{circular.titulo}", fontsize=30, color=(1, 0, 0))  # Rojo
    y += 20
    page.insert_text((80, y), f"Solicitante: {circular.Solicitante}", fontsize=12, color=(0, 0, 1))  # Azul
    y += 20
    page.insert_text((80, y), f"Fecha Inicio: {circular.fechaInicioTrabajo.strftime('%d-%m-%Y %H:%M')}", fontsize=12)
    page.insert_text((380, y), f"Fecha Fin: {circular.fechaFinTrabajo.strftime('%d-%m-%Y %H:%M')}", fontsize=12)
    y += 20

    # Información adicional
    page.insert_text((80, y), "Responsables: ", fontsize=12)
    y += 20
    responsables = "\n".join([f"{r} \n Teléfono: {r.telefono}, interno: {r.interno}, celular: {r.celular}" for r in circular.responsable.all()])
    page.insert_text((100, y), responsables, fontsize=12)
    y += 120

    # Insertar descripción con salto de página si es necesario
    descripcion = wrap(circular.descripcion, width=80)
    page.insert_text((80, y), "Descripción: ", fontsize=12)
    y += 20
    y_pos = y  
    max_y = 750  
    margen_superior = 100  

    for linea in descripcion:
        if y_pos >= max_y:
            page = doc.new_page()  
            y_pos = margen_superior  
        page.insert_text((100, y_pos), linea, fontsize=12)  
        y_pos += 20  

    # Guardar el PDF generado
    doc.save(output_pdf)
    doc.close()
    
    return output_pdf  # Devuelve la ruta del PDF generado
def editar_pdf(request, id):
    """
    Vista que genera el PDF y lo devuelve para su visualización en el navegador.
    """
    circular = get_object_or_404(Circular, id=id)

    # Generar el PDF y obtener la ruta del archivo
    output_pdf = generar_pdf(circular)

    # Devolver el PDF para mostrarlo en el navegador
    with open(output_pdf, "rb") as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{circular.titulo}.pdf"'  # Muestra en la misma pestaña
        return response

def enviar_mail(request, id):
    """
    Vista que maneja el envío de correos con la circular adjunta.
    """
    circular = get_object_or_404(Circular, id=id)
    
    # Obtener la agenda
    agenda = Agenda.objects.all()
    
    # Ordenar por 'subGerencia'
    subGerencia_sorted = sorted(agenda, key=lambda x: x.subGerencia)
    grupo_sorted = sorted(agenda, key=lambda x: x.grupo)
    
    # Eliminar duplicados por 'subGerencia' usando groupby
    subGerencia_unique = [next(group) for key, group in groupby(subGerencia_sorted, key=lambda x: x.subGerencia)]
    grupo_unique = [next(group) for key, group in groupby(grupo_sorted, key=lambda x: x.grupo)]

    # Generamos el PDF de la circular
    output_pdf = generar_pdf(circular)  

    if request.method == "POST":
        # Obtener los IDs de los destinatarios seleccionados manualmente
        # destinatarios_ids = request.POST.getlist("destinatarios")  # Destinatarios seleccionados manualmente
        # destinatarios = Agenda.objects.filter(id__in=destinatarios_ids).values_list('email', flat=True)
        # Obtener los IDs de los destinatarios seleccionados manualmente
        destinatarios_ids = request.POST.getlist("destinatarios")  # Destinatarios seleccionados manualmente
        destinatarios = list(Agenda.objects.filter(id__in=destinatarios_ids).values_list('email', flat=True))

        
        # Obtener los destinatarios de la subgerencia seleccionada
        subgerencia = request.POST.get("subgerencia")  # Suponiendo que el ID de subgerencia viene en el formulario
        if subgerencia:
            subgerencia_destinatarios = Agenda.objects.filter(subGerencia=subgerencia).values_list('email', flat=True)
        else:
            subgerencia_destinatarios = []

        # Obtener los destinatarios de la grupo seleccionada
        grupo = request.POST.get("grupo")  # Suponiendo que el ID de subgerencia viene en el formulario
        if grupo:
            grupo_destinatarios = Agenda.objects.filter(grupo=grupo).values_list('email', flat=True)
        else:
            grupo_destinatarios = []

        # Combinar ambos grupos de destinatarios y eliminar duplicados
        all_destinatarios = list(set(destinatarios).union(set(subgerencia_destinatarios)))  
        all_destinatarios = list(set(all_destinatarios).union(set(grupo_destinatarios)))
        print("all_destinatarios ",all_destinatarios)

        # Verificar si hay destinatarios
        if not all_destinatarios:
            messages.error(request, "El destinatario es obligatorio.")
            return render(request, "enviar_mail.html", {
                "error": "No se seleccionaron destinatarios.", 
                "circular": circular,
                "agenda": agenda,
                'subGerencias': subGerencia_unique,
                'grupos': grupo_unique,
            })
        i=1
        print(i)
        i += 1
        # Convertir los emails en una lista separada por ";"
        destinatarios_str = "; ".join(all_destinatarios)
        print(i)
        i += 1
        # Obtener el asunto y mensaje
        asunto = request.POST.get("asunto")
        mensaje = request.POST.get("mensaje")

        try:
            print(i)
            i += 1
            
            print(i ,"4?")
            i += 1

            # Iniciar la conexión con Outlook
            # outlook = win32.Dispatch("Outlook.Application")
            try:
                pythoncom.CoInitialize()    
                outlook = win32.Dispatch("Outlook.Application")
                print("Outlook se inició correctamente.")
            except Exception as e:
                print(f"Error al iniciar Outlook: {e}")
            print(i)
            i += 1
            mail = outlook.CreateItem(0)  # 0 = Correo
            
            print(i)
            i += 1
            # Configurar correo
            mail.To = destinatarios_str
            mail.Subject = asunto
            mail.Body = mensaje

            # Adjuntar el archivo PDF
            mail.Attachments.Add(output_pdf)
            
            print(i)
            i += 1
            # Enviar el correo
            mail.Send()
            print("mail: ",mail)
            messages.success(request, "Correo enviado con éxito.")

            return redirect("enviar_mail", id=circular.id)  # Redirigir a la misma vista para mostrar el mensaje

        except Exception as e:
            messages.error(request, f"Error al enviar el correo: {str(e)}")

    # if request.method == "POST":
    #     destinatarios_ids = request.POST.getlist("destinatarios")  # Obtener IDs de los destinatarios
    #     destinatarios = Agenda.objects.filter(id__in=destinatarios_ids).values_list('email', flat=True)
    #     # destinatario = request.POST.get("destinatario")
    #     asunto = request.POST.get("asunto")
    #     mensaje = request.POST.get("mensaje")

    #     if not destinatarios:
    #         messages.error(request, "El destinatario es obligatorio.")
    #         return render(request, "enviar_mail.html", {
    #             "error": "No se seleccionaron destinatarios.", 
    #             "agenda": agenda,
    #             "circular": circular
    #             })
        
    #     # Convertir los emails en una lista separada por ";"
    #     destinatarios_str = "; ".join(destinatarios)

    #     try:
    #         pythoncom.CoInitialize()

    #         # Iniciar la conexión con Outlook
    #         outlook = win32.Dispatch("Outlook.Application")
    #         mail = outlook.CreateItem(0)  # 0 = Correo

    #         # Configurar correo
    #         mail.To = destinatarios_str
    #         mail.Subject = asunto
    #         mail.Body = mensaje

    #         # Adjuntar el archivo PDF
    #         mail.Attachments.Add(output_pdf)

    #         # Enviar el correo
    #         mail.Send()
    #         messages.success(request, "Correo enviado con éxito.")

    #         return redirect("enviar_mail", id=circular.id)  # Redirigir a la misma vista para mostrar el mensaje

    #     except Exception as e:
    #         messages.error(request, f"Error al enviar el correo: {str(e)}")

    return render(request, "enviar_mail.html", {
        "circular": circular,
        "agenda": agenda,
        'subGerencias': subGerencia_unique,
        'grupos': grupo_unique,
        })
    
# def enviar_correo_outlook(destinatario, asunto, cuerpo, adjunto):
#     try:
#         # Inicializar Outlook
#         outlook = win32com.client.Dispatch("Outlook.Application")
#         mail = outlook.CreateItem(0)  # 0 = Correo

#         # Configurar correo
#         mail.To = destinatario
#         mail.Subject = asunto
#         mail.Body = cuerpo

#         # Adjuntar archivo
#         if os.path.exists(adjunto):
#             mail.Attachments.Add(adjunto)
#         else:
#             return HttpResponse("Error: No se encontró el archivo adjunto.")

#         # Enviar el correo
#         mail.Send()
#         return HttpResponse("Correo enviado correctamente.")
    
#     except Exception as e:
#         return HttpResponse(f"Error al enviar el correo: {e}")