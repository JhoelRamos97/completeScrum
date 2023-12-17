from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import FileResponse
from datetime import date, timedelta
from .forms import FormBodega, FormTipoActivo, FormActivo
from .models import Bodega, Tipo_activo, Activo, Movimiento
from datetime import datetime, timedelta
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Create your views here.
def signin(req):
    #si ya se inicio secion, redirige a la pagina de inicio
    if req.user.is_authenticated:
        return redirect('/inicio')
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
        try:
            form = FormActivo(req.POST)
            if form.is_valid():
                form.save()
                activo = Activo.objects.last()
                movimiento = Movimiento(
                    fecha=datetime.now(),
                    nombre_activo=activo.nombre,
                    cantidad=activo.cantidad,
                    nombre_bodega=activo.bodega.nombre,
                    tipo_movimiento='AD_ac',
                    user=req.user
                )
                movimiento.save()
                messages.success(req, f'Se agrego el activo "{activo.nombre}" correctamente.')
                return redirect('/activos/')
        except Exception as e:
            messages.error(req, f'No se pudo agregar el activo. Error: {str(e)}')

    data = {'form': form, 'accion': 'Agregar', 'descripcion': 'Agregue los atribulos del activos que desea añadir al inventario.'}
    return render(req, 'activo/add_activo.html', data)

def edit_activo(req, id):
    activo = Activo.objects.get(id=id)
    form = FormActivo(instance=activo)

    # Formatear las fechas en el formato 'YYYY-MM-DD'
    formatted_fecha_contable = activo.fecha_contable.strftime('%Y-%m-%d')
    formatted_fecha_adquisicion = activo.fecha_adquisicion.strftime('%Y-%m-%d')
    formatted_fecha_descontinuacion = activo.fecha_descontinuacion.strftime('%Y-%m-%d')

    # Actualizar el diccionario initial del formulario
    form.initial.update({
        'fecha_contable': formatted_fecha_contable,
        'fecha_adquisicion': formatted_fecha_adquisicion,
        'fecha_descontinuacion': formatted_fecha_descontinuacion,
    })

    if req.method == "POST":
        try:
            form = FormActivo(req.POST, instance=activo)
            if form.is_valid():
                form.save()
                movimiento = Movimiento(
                    fecha=datetime.now(),
                    nombre_activo=activo.nombre,
                    cantidad=activo.cantidad,
                    nombre_bodega=activo.bodega.nombre,
                    tipo_movimiento='ED_ac',
                    user=req.user
                    )
                movimiento.save()
                messages.success(req, f'Se actualizó el activo "{activo.nombre}" correctamente.')
                return redirect('/activos/')
        except Exception as e:
            messages.error(req, f'No se pudo actualizar el activo. Error: {str(e)}')

    data = {'form': form, 'accion': 'Actualizar', 'descripcion': 'Cambie los atributos del activo que desea actualizar.'}
    return render(req, 'activo/add_activo.html', data)

@login_required
def del_activo(req, id):
    activo = Activo.objects.get(id=id)
    try:
        movimiento = Movimiento(
            fecha=datetime.now(),
            nombre_activo=activo.nombre,
            cantidad=activo.cantidad,
            nombre_bodega=activo.bodega.nombre,
            tipo_movimiento='DE_ac',
            user=req.user
            )
        movimiento.save()
        activo.delete()
        messages.success(req, f'Se eliminó el activo "{activo.nombre}" correctamente.')
    except Exception as e:
        messages.error(req, f'No se pudo eliminar el activo. Error: {str(e)}')

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
        try:
            form = FormBodega(req.POST)
            if form.is_valid():
                form.save()
                bodega = Bodega.objects.last()
                movimiento = Movimiento(
                    fecha=datetime.now(),
                    nombre_activo=None,
                    cantidad=None,
                    nombre_bodega=bodega.nombre,
                    tipo_movimiento='AD_bo',
                    user=req.user
                    )
                movimiento.save()
                messages.success(req, f'Se agrego la bodega "{bodega.nombre}" correctamente.')
                return redirect('/bodegas/')
        except Exception as e:
            messages.error(req, f'No se pudo agregar la bodega. Error: {str(e)}')

    data = {'form': form, 'accion': 'Agregar', 'descripcion': 'Agregue los atribulos de la bodega que desea añadir.'}
    return render(req, 'bodega/add_bodega.html', data)

@login_required
def edit_bodega(req, id):
    bodega = Bodega.objects.get(id=id)
    form = FormBodega(instance=bodega)

    if req.method == "POST":
        try:
            form = FormBodega(req.POST, instance=bodega)
            if form.is_valid():
                form.save()
                movimiento = Movimiento(
                    fecha=datetime.now(),
                    nombre_activo=None,
                    cantidad=None,
                    nombre_bodega=bodega.nombre,
                    tipo_movimiento='ED_bo',
                    user=req.user
                    )
                movimiento.save()
                messages.success(req, f'Se actualizó la bodega "{bodega.nombre}" correctamente.')
                return redirect(f'/bodega/{id}/')
        except Exception as e:
            messages.error(req, f'No se pudo actualizar la bodega. Error: {str(e)}')

    data = {'form': form, 'accion': 'Actualizar', 'descripcion': 'Cambie los atribulos de la bodega que desea actualizar.'}
    return render(req, 'bodega/add_bodega.html', data)

@login_required
def del_bodega(req, id):
    try:
        bodega = Bodega.objects.get(id=id)
        movimiento = Movimiento(
            fecha=datetime.now(),
            nombre_activo=None,
            cantidad=None,
            nombre_bodega=bodega.nombre,
            tipo_movimiento='DE_bo',
            user=req.user
            )
        movimiento.save()
        bodega.delete()
        messages.success(req, f'Se eliminó la bodega "{bodega.nombre}" correctamente.')
    except Exception as e:
        messages.error(req, f'No se pudo eliminar la bodega. Error: {str(e)}')
    
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
        try:
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
                messages.success(req, f'Se agrego el tipo de activo "{form.cleaned_data.get("nombre")}" correctamente.')
                return redirect('/tipos-de-activos/')
        except Exception as e:
            messages.error(req, f'No se pudo agregar el tipo de activo. Error: {str(e)}')

    data = {'form': form, 'accion': 'Agregar', 'descripcion': 'Agregue los atribulos del tipo de activo que desea añadir.'}
    return render(req, 'tipo_activo/add_tipo_activo.html', data)

@login_required
def edit_tipo_activo(req, id):
    tipo_activo = Tipo_activo.objects.get(id=id)
    form = FormTipoActivo(instance=tipo_activo)

    if req.method == "POST":
        try:
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
                return redirect('/tipos-de-activos/')
            messages.success(req, f'Se actualizó el tipo de activo "{tipo_activo.nombre}" correctamente.')
        except Exception as e:
            messages.error(req, f'No se pudo actualizar el tipo de activo. Error: {str(e)}')

    data = {'form': form, 'accion': 'Actualizar', 'descripcion': 'Cambie los atribulos del tipo de activo que desea actualizar.'}
    return render(req, 'tipo_activo/add_tipo_activo.html', data)

@login_required
def del_tipo_activo(req, id):
    try:
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
        messages.success(req, f'Se eliminó el tipo de activo "{tipo_activo.nombre}" correctamente.')
    except Exception as e:
        messages.error(req, f'No se pudo eliminar el tipo de activo. Error: {str(e)}')

    return redirect('read_tipo_activo')
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
        try:
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
        except Exception as e:
            messages.error(req, f'No se pudo mover el activo. Error: {str(e)}')
    
    data = {'bodega': bodega, 'activos': activos}
    return render(req, 'activo_bodega/add_activo_bodega.html', data)

@login_required
def edit_activo_bodega(req, id_bodega, id_activo):
    bodega = Bodega.objects.get(id=id_bodega)
    bodegas = Bodega.objects.all()
    activo = Activo.objects.get(id=id_activo)

    if req.method == 'POST':
        try:
            id_bodega_selecionada = req.POST.get('bodega_seleccionada')
            bodega_selecionada = Bodega.objects.get(id=id_bodega_selecionada)
            activo.bodega = bodega_selecionada
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
            return redirect(f'/bodega/{id_bodega_selecionada}/')
        except Exception as e:
            messages.error(req, f'No se pudo mover el activo. Error: {str(e)}')
    
    data = {'bodegas': bodegas, 'activo': activo, 'bodega': bodega}
    return render(req, 'activo_bodega/edit_activo_bodega.html', data)

@login_required
def del_activo_bodega(req, id_bodega, id_activo):
    activo = Activo.objects.get(id=id_activo)
    activo.bodega = None
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

@login_required
def read_movimiento(req):
    return render(req, 'read_movimiento.html')

@login_required
def read_movimiento_dia(req):
    fecha_actual = date.today()
    movimientos = Movimiento.objects.filter(fecha__date=fecha_actual).order_by('-fecha')
    data = {'movimientos': movimientos}
    return render(req, 'read_movimiento.html', data)

@login_required
def read_movimiento_semana(req):
    fecha_actual = date.today()
    inicio_semana = fecha_actual - timedelta(days=fecha_actual.weekday())
    fin_semana = inicio_semana + timedelta(days=6)
    movimientos = Movimiento.objects.filter(fecha__date__range=[inicio_semana, fin_semana]).order_by('-fecha')
    data = {'movimientos': movimientos}
    return render(req, 'read_movimiento.html', data)

@login_required
def read_movimiento_mes(req):
    fecha_actual = date.today()
    primer_dia_mes = fecha_actual.replace(day=1)
    ultimo_dia_mes = (primer_dia_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    movimientos = Movimiento.objects.filter(fecha__date__range=[primer_dia_mes, ultimo_dia_mes]).order_by('-fecha')
    data = {'movimientos': movimientos}
    return render(req, 'read_movimiento.html', data)

@login_required
def read_movimiento_all(req):
    movimientos = Movimiento.objects.all().order_by('-fecha')
    data = {'movimientos': movimientos}
    return render(req, 'read_movimiento.html', data)


@login_required
def generar_pdf(req):
    movimientos = Movimiento.objects.all().order_by('-fecha')
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    # Añade un título al PDF
    titulo = Paragraph(f'Informe de todos los movimientos del sistema de inventario durante el ultimo mes', styles['Title'])
    elements.append(titulo)
    for m in movimientos:
        if m.tipo_movimiento == 'AD_ac':
            tipo_movimiento = 'Se agrego un activo al inventario'
        elif m.tipo_movimiento == 'ED_ac':
            tipo_movimiento = 'Se actualizo un activo en inventario'
        elif m.tipo_movimiento == 'DE_ac':
            tipo_movimiento = 'Se elimino un activo del inventario'
        elif m.tipo_movimiento == 'AD_bo':
            tipo_movimiento = 'Se registro una nueva bodega'
        elif m.tipo_movimiento == 'ED_bo':
            tipo_movimiento = 'Se actualizaron datos de una bodega'
        elif m.tipo_movimiento == 'DE_bo':
            tipo_movimiento = 'Se elimino una bodega del registro'
        elif m.tipo_movimiento == 'AD_ta':
            tipo_movimiento = 'Se agrego un nuevo tipo de activo'
        elif m.tipo_movimiento == 'ED_ta':
            tipo_movimiento = 'Se actualizaron datos de un tipo de activo'
        elif m.tipo_movimiento == 'DE_ta':
            tipo_movimiento = 'Se elimino un tipo de activo del registro'
        elif m.tipo_movimiento == 'AD_ab':
            tipo_movimiento = 'Se agrego un activo a una bodega'
        elif m.tipo_movimiento == 'ED_ab':
            tipo_movimiento = 'Se movio un activo de una bodega a otra bodega'
        elif m.tipo_movimiento == 'DE_ab':
            tipo_movimiento = 'Se quito un activo de una bodega'
        else:
            tipo_movimiento = 'Desconocido'
        if m.nombre_activo == None:
            nombre_activo = 'Ninguno'
        else:
            nombre_activo = m.nombre_activo
        if m.nombre_bodega == None:
            nombre_bodega = 'Ninguno'
        else:
            nombre_bodega = m.nombre_bodega
        if m.cantidad == None:
            cantidad = 'Ninguno'
        else:
            cantidad = m.cantidad
        fecha = m.fecha.strftime("%d/%m/%Y %H:%M:%S")
        # Añade un párrafo al PDF
        texto = f'Fecha: {fecha} | Tipo de movimiento: {tipo_movimiento} | Cantidad: {cantidad} | Nombre del activo: {nombre_activo} | Nombre de la bodega: {nombre_bodega} | Usuario: {m.user.username}'
        parrafo = Paragraph(texto, styles['Normal'])
        elements.append(parrafo)
        # Añade un espacio al PDF
        elements.append(Spacer(1, 12))
    # Construye el PDF
    doc.build(elements)
    # Configura la respuesta con el PDF
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Informe de sistema de movimientos.pdf")

@login_required
def edit_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualiza la sesión del usuario para evitar cerrar sesión
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente.')
            return redirect('/inicio/')
        else:
            messages.error(request, 'Por favor, corrija los errores.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'edit_password.html', {'form': form})
