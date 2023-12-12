from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import FileResponse
from .forms import FormBodega, FormTipoActivo, FormActivo
from .models import Bodega, Tipo_activo, Activo, Movimiento
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Create your views here.
def signin(req):
    if req.method == 'POST':
        form = AuthenticationForm(req, req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(req, username=username, password=password)
            if user is not None:
                login(req, user)
                return redirect('/inicio')
            else:
                messages.error(req, 'Nombre de usuario o contraseña incorrectos.')
        else:
            messages.error(req, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(req, 'login.html', {'form': form})

def singout(req):
    logout(req)
    return redirect('/')

@login_required
def inicio(req):
    return render(req, 'inicio.html')

######################## Activo #######################
#                                                     #
@login_required
def read_activo(req):
    activos = Activo.objects.all()
    data = {'activos': activos}
    return render(req, 'activo/read_activo.html', data)

@login_required
def add_activo(req):
    form = FormActivo()

    if req.method == "POST":
        form = FormActivo(req.POST)
        if form.is_valid():
            print(form.bodega)
            form.save()
            activo = Activo.objects.last().id
            if activo.bodega == None:
                movimiento = Movimiento(
                    fecha=datetime.now(),
                    cantidad=activo.cantidad,
                    nombre_activo=activo.nombre,
                    nombre_bodega=None,
                    tipo_movimiento='AD_ac',
                    user=req.user
                )
            else:
                movimiento = Movimiento(
                    fecha=datetime.now(),
                    cantidad=activo.cantidad,
                    nombre_activo=activo.nombre,
                    nombre_bodega=activo.bodega.nombre,
                    tipo_movimiento='AD_ac',
                    user=req.user
                )
            movimiento.save()
            return redirect('/activos/')

    data = {'form': form, 'accion': 'Agregar', 'descripcion': 'Agregue los atribulos del activos que desea añadir al inventario.'}
    return render(req, 'activo/add_activo.html', data)

@login_required
def edit_activo(req, id):
    activo = Activo.objects.get(id=id)
    form = FormActivo(instance=activo)

    if req.method == "POST":
        form = FormActivo(req.POST, instance=activo)
        if form.is_valid():
            form.save()
            if activo.bodega == None:
                movimiento = Movimiento(
                    fecha=datetime.now(),
                    cantidad=activo.cantidad,
                    nombre_activo=activo.nombre,
                    nombre_bodega=None,
                    tipo_movimiento='ED_ac',
                    user=req.user
                )
            else:
                movimiento = Movimiento(
                    fecha=datetime.now(),
                    cantidad=activo.cantidad,
                    nombre_activo=activo.nombre,
                    nombre_bodega=activo.bodega.nombre,
                    tipo_movimiento='ED_ac',
                    user=req.user
                    )
            movimiento.save()
            return redirect('/activos/')

    data = {'form': form, 'accion': 'Actualizar', 'descripcion': 'Cambie los atribulos del activo que desea actualizar.'}
    return render(req, 'activo/add_activo.html', data)

@login_required
def del_activo(req, id):
    activo = Activo.objects.get(id=id)
    if activo.bodega == None:
        movimiento = Movimiento(
            fecha=datetime.now(),
            cantidad=activo.cantidad,
            nombre_activo=activo.nombre,
            nombre_bodega=None,
            tipo_movimiento='DE_ac',
            user=req.user
            )
    else:
        movimiento = Movimiento(
            fecha=datetime.now(),
            cantidad=activo.cantidad,
            nombre_activo=activo.nombre,
            nombre_bodega=activo.bodega.nombre,
            tipo_movimiento='DE_ac',
            user=req.user
            )
    movimiento.save()
    activo.delete()
    return redirect('/activos/')
#                                                     #
#######################################################

######################## Bodega #######################
#                                                     #
@login_required
def read_bodega(req):
    bodegas = Bodega.objects.all()
    data = {'bodegas': bodegas}
    return render(req, 'bodega/read_bodega.html', data)

@login_required
def add_bodega(req):
    form = FormBodega()

    if req.method == "POST":
        form = FormBodega(req.POST)
        if form.is_valid():
            form.save()
            bodega = Bodega.objects.last().id
            movimiento = Movimiento(
                fecha=datetime.now(),
                cantidad=None,
                nombre_activo=None,
                nombre_bodega=bodega.nombre,
                tipo_movimiento='AD_bo',
                user=req.user
                )
            movimiento.save()
            return redirect('/bodegas/')

    data = {'form': form, 'accion': 'Agregar', 'descripcion': 'Agregue los atribulos de la bodega que desea añadir.'}
    return render(req, 'bodega/add_bodega.html', data)

@login_required
def edit_bodega(req, id):
    bodega = Bodega.objects.get(id=id)
    form = FormBodega(instance=bodega)

    if req.method == "POST":
        form = FormBodega(req.POST, instance=bodega)
        if form.is_valid():
            form.save()
            movimiento = Movimiento(
                fecha=datetime.now(),
                cantidad=None,
                nombre_activo=None,
                nombre_bodega=bodega.nombre,
                tipo_movimiento='ED_bo',
                user=req.user
                )
            movimiento.save()
            return redirect('/bodegas/')

    data = {'form': form, 'accion': 'Actualizar', 'descripcion': 'Cambie los atribulos de la bodega que desea actualizar.'}
    return render(req, 'bodega/add_bodega.html', data)

@login_required
def del_bodega(req, id):
    bodega = Bodega.objects.get(id=id)
    movimiento = Movimiento(
        fecha=datetime.now(),
        cantidad=None,
        nombre_activo=None,
        nombre_bodega=bodega.nombre,
        tipo_movimiento='DE_bo',
        user=req.user
        )
    movimiento.save()
    bodega.delete()
    return redirect('/bodegas/')
#                                                     #
#######################################################

##################### Tipo Activo #####################
#                                                     #
@login_required
def read_tipo_activo(req):
    tipos_activos = Tipo_activo.objects.all()
    data = {'tipos_activos': tipos_activos}
    return render(req, 'tipo_activo/read_tipo_activo.html', data)

@login_required
def add_tipo_activo(req):
    form = FormTipoActivo()

    if req.method == "POST":
        form = FormTipoActivo(req.POST)
        if form.is_valid():
            form.save()
            movimiento = Movimiento(
                fecha=datetime.now(),
                cantidad=None,
                nombre_activo=None,
                nombre_bodega=None,
                tipo_movimiento='AD_ta',
                user=req.user
                )
            movimiento.save()
            return redirect('/tipos-de-activos/')

    data = {'form': form, 'accion': 'Agregar', 'descripcion': 'Agregue los atribulos del tipo de activo que desea añadir.'}
    return render(req, 'tipo_activo/add_tipo_activo.html', data)

@login_required
def edit_tipo_activo(req, id):
    tipo_activo = Tipo_activo.objects.get(id=id)
    form = FormTipoActivo(instance=tipo_activo)

    if req.method == "POST":
        form = FormTipoActivo(req.POST, instance=tipo_activo)
        if form.is_valid():
            form.save()
            movimiento = Movimiento(
                fecha=datetime.now(),
                cantidad=None,
                nombre_activo=None,
                nombre_bodega=None,
                tipo_movimiento='ED_ta',
                user=req.user
                )
            movimiento.save()
            return redirect('/tipos_de_activos/')

    data = {'form': form, 'accion': 'Actualizar', 'descripcion': 'Cambie los atribulos del tipo de activo que desea actualizar.'}
    return render(req, 'tipo_activo/add_tipo_activo.html', data)

@login_required
def del_tipo_activo(req, id):
    tipo_activo = Tipo_activo.objects.get(id=id)
    tipo_activo.delete()
    movimiento = Movimiento(
        fecha=datetime.now(),
        cantidad=None,
        nombre_activo=None,
        nombre_bodega=None,
        tipo_movimiento='DE_ta',
        user=req.user
        )
    movimiento.save()
    return read_tipo_activo(req)
#                                                     #
#######################################################

#################### Activo Bodega ####################
#                                                     #
@login_required
def read_activo_bodega(req, id):
    bodega = Bodega.objects.get(id=id)
    activos = Activo.objects.filter(bodega=id)
    data = {'bodega': bodega, 'activos': activos}
    return render(req, 'activo_bodega/read_activo_bodega.html', data)

@login_required
def add_activo_bodega(req, id):
    bodega = Bodega.objects.get(id=id)
    activos = Activo.objects.all()

    if req.method == 'POST':
        activos_seleccionados = req.POST.getlist('activo_seleccionado')
        Activo.objects.filter(id__in=activos_seleccionados).update(bodega=id)
        
        for activo_id in activos_seleccionados:
            activo_actual = Activo.objects.get(id=activo_id)
            movimiento = Movimiento(
                fecha=datetime.now(),
                cantidad=activo_actual.cantidad,
                nombre_activo=activo_actual.nombre,
                nombre_bodega=bodega.nombre,
                tipo_movimiento='AD_ab',
                user=req.user
            )
            movimiento.save()
        
        return redirect(f'/bodega/{id}/')
    
    data = {'bodega': bodega, 'activos': activos}
    return render(req, 'activo_bodega/add_activo_bodega.html', data)

@login_required
def edit_activo_bodega(req, id_bodega, id_activo):
    bodega = Bodega.objects.get(id=id_bodega)
    bodegas = Bodega.objects.all()
    activo = Activo.objects.get(id=id_activo)

    if req.method == 'POST':
        bodega_selecionada = req.POST.get('bodega_seleccionada')
        activo.id_bodega = bodega_selecionada
        activo.save()
        movimiento = Movimiento(
            fecha=datetime.now(),
            cantidad=activo.cantidad,
            nombre_activo=activo.nombre,
            nombre_bodega=bodega.nombre,
            tipo_movimiento='ED_ab',
            user=req.user
            )
        movimiento.save()
        return redirect(f'/bodega/{bodega_selecionada.id}/')
    
    data = {'bodegas': bodegas, 'activo': activo, 'bodega': bodega}
    return render(req, 'activo_bodega/edit_activo_bodega.html', data)

@login_required
def del_activo_bodega(req, id_bodega, id_activo):
    activo = Activo.objects.get(id=id_activo)
    activo.id_bodega = None
    movimiento = Movimiento(
        fecha=datetime.now(),
        cantidad=activo.cantidad,
        nombre_activo=activo.nombre,
        tipo_movimiento='DE_ab',
        user=req.user
        )
    movimiento.save()
    activo.save()
    return redirect(f'/bodega/{id_bodega}/')
#                                                     #
#######################################################

def read_movimiento(req):
    movimientos = Movimiento.objects.all()
    data = {'movimientos': movimientos}
    return render(req, 'read_movimiento.html', data)

def generar_pdf(req, fecha_inicio, fecha_final):
    movimientos = Movimiento.objects.all()
    print(movimientos)
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Añade un título al PDF
    titulo = Paragraph(f'Informe de sistema de inventario desde {fecha_inicio} hasta {fecha_final}', styles['Title'])
    elements.append(titulo)

    # Construye el PDF
    doc.build(elements)

    # Configura la respuesta con el PDF
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Informe de sistema de ventas.pdf")