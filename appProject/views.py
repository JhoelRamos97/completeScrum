from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import FormBodega, FormTipoActivo, FormActivo
from .models import Bodega, Tipo_activo, Activo

# Create your views here.
def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/inicio')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def singout(request):
    return redirect('singin')

@login_required
def inicio(request):
    return render(request, 'inicio.html')

######################## Activo #######################
#                                                     #
@login_required
def read_activo(request):
    activos = Activo.objects.all()
    data = {'activos': activos}
    return render(request, 'activo/read_activo.html', data)

def add_activo(request):
    form = FormActivo()

    if request.method == "POST":
        form = FormActivo(request.POST)
        if form.is_valid():
            form.save()
            return read_activo(request)

    data = {'form': form, 'accion': 'Agregar', 'descripcion': 'Agregue los atribulos del activos que desea añadir al inventario.'}
    return render(request, 'activo/add_activo.html', data)

def edit_activo(request, id):
    activo = Activo.objects.get(id=id)
    form = FormActivo(instance=activo)

    if request.method == "POST":
        form = FormActivo(request.POST, instance=activo)
        if form.is_valid():
            form.save()
            return read_activo(request)

    data = {'form': form, 'accion': 'Actualizar', 'descripcion': 'Cambie los atribulos del activo que desea actualizar.'}
    return render(request, 'activo/edit_activo.html', data)

def del_activo(request, id):
    activo = Activo.objects.get(id=id)
    activo.delete()
    return read_activo(request)
#                                                     #
#######################################################

######################## Bodega #######################
#                                                     #
@login_required
def read_bodega(request):
    bodegas = Bodega.objects.all()
    data = {'bodegas': bodegas}
    return render(request, 'bodega/read_bodega.html', data)

def add_bodega(request):
    form = FormBodega()

    if request.method == "POST":
        form = FormBodega(request.POST)
        if form.is_valid():
            form.save()
            return read_bodega(request)

    data = {'form': form, 'accion': 'Agregar', 'descripcion': 'Agregue los atribulos de la bodega que desea añadir.'}
    return render(request, 'bodega/add_bodega.html', data)

def edit_bodega(request, id):
    bodega = Bodega.objects.get(id=id)
    form = FormBodega(instance=bodega)

    if request.method == "POST":
        form = FormBodega(request.POST, instance=bodega)
        if form.is_valid():
            form.save()
            return read_bodega(request)

    data = {'form': form, 'accion': 'Actualizar', 'descripcion': 'Cambie los atribulos de la bodega que desea actualizar.'}
    return render(request, 'bodega/edit_bodega.html', data)

def del_bodega(request, id):
    bodega = Bodega.objects.get(id=id)
    bodega.delete()
    return read_bodega(request)
#                                                     #
#######################################################

##################### Tipo Activo #####################
#                                                     #
@login_required
def read_tipo_activo(request):
    tipos_activos = Tipo_activo.objects.all()
    data = {'tipos_activos': tipos_activos}
    return render(request, 'tipo_activo/read_tipo_activo.html', data)

def add_tipo_activo(request):
    form = FormTipoActivo()

    if request.method == "POST":
        form = FormTipoActivo(request.POST)
        if form.is_valid():
            form.save()
            return read_tipo_activo(request)

    data = {'form': form, 'accion': 'Agregar', 'descripcion': 'Agregue los atribulos del tipo de activo que desea añadir.'}
    return render(request, 'tipo_activo/add_tipo_activo.html', data)

def edit_tipo_activo(request, id):
    tipo_activo = Tipo_activo.objects.get(id=id)
    form = FormTipoActivo(instance=tipo_activo)

    if request.method == "POST":
        form = FormTipoActivo(request.POST, instance=tipo_activo)
        if form.is_valid():
            form.save()
            return read_tipo_activo(request)

    data = {'form': form, 'accion': 'Actualizar', 'descripcion': 'Cambie los atribulos del tipo de activo que desea actualizar.'}
    return render(request, 'tipo_activo/edit_tipo_activo.html', data)

def del_tipo_activo(request, id):
    tipo_activo = Tipo_activo.objects.get(id=id)
    tipo_activo.delete()
    return read_tipo_activo(request)
#                                                     #
#######################################################