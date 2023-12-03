from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
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

@login_required
def inicio(request):
    return render(request, 'inicio.html')

@login_required
def read_activos(request):
    activos = Activo.objects.all()
    data = {'activos': activos}
    return render(request, 'activos/read_activo.html', data)

@login_required
def read_bodegas(request):
    bodegas = Bodega.objects.all()
    data = {'bodegas': bodegas}
    return render(request, 'bodegas/read_bodega.html', data)

@login_required
def read_tipos_activos(request):
    tipos_activos = Tipo_activo.objects.all()
    data = {'tipos_activos': tipos_activos}
    return render(request, 'tipo_activos/read_tipo_activo.html', data)