from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import FileResponse
from datetime import date, timedelta
from .forms import FormBodega, FormTipoActivo, FormActivo
from .models import Bodega, Tipo_activo, Activo, Movimiento, Activo_bodega
from datetime import datetime, timedelta
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def is_superuser(user):
    return user.is_superuser

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
    user = req.user
    activo_bodega = Activo_bodega.objects.all()
    tipo_activo = Tipo_activo.objects.all()
    if tipo_activo.count() == 0:
        messages.error(req, 'No se puede agregar un activo sin ningun tipo de activo registrado. Por favor, agregue un tipo de activo.')
    activos = Activo.objects.all()
    data = {'activos': activos, 'user': user, 'activo_bodega': activo_bodega, 'tipo_activo': tipo_activo}
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
                bodega_seleccionada = form.cleaned_data.get('bodega')
                activo_bodega = Activo_bodega(
                    estado = True,
                    activo = activo,
                    bodega = bodega_seleccionada,
                )
                activo_bodega.save()
                activo_bodega = Activo_bodega.objects.last()
                if activo_bodega.bodega.nombre == 'Sin bodega':
                    movimiento = Movimiento(
                        fecha           = datetime.now(),
                        tipo_movimiento = 'AS',
                        cantidad        = activo.cantidad,
                        activo_bodega   = activo_bodega,
                        user            = req.user
                    )
                else:
                    movimiento = Movimiento(
                        fecha           = datetime.now(),
                        tipo_movimiento = 'AD',
                        cantidad        = activo.cantidad,
                        activo_bodega   = activo_bodega,
                        user            = req.user
                    )
                movimiento.save()
                messages.success(req, f'Se agrego el activo "{activo.nombre}" correctamente.')
                return redirect('/activos/')
            else:
                messages.error(req, f'Los datos ingresados no son validos.')
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
                bodega_seleccionada = form.cleaned_data.get('bodega')
                # poner el estado en false a todos los activos_bodega que tengan el activo usando filter
                activo_bodega = Activo_bodega.objects.filter(activo=activo)
                for ab in activo_bodega:
                    ab.estado = False
                    ab.save()
                
                activo_bodega = Activo_bodega(
                    estado = True,
                    activo = activo,
                    bodega = bodega_seleccionada,
                )
                activo_bodega.save()
                if activo_bodega.bodega.nombre == 'Sin bodega':
                    movimiento = Movimiento(
                        fecha           = datetime.now(),
                        tipo_movimiento = 'ES',
                        cantidad        = activo.cantidad,
                        activo_bodega   = activo_bodega,
                        user            = req.user
                    )
                else:
                    movimiento = Movimiento(
                        fecha           = datetime.now(),
                        tipo_movimiento = 'ED',
                        cantidad        = activo.cantidad,
                        activo_bodega   = activo_bodega,
                        user            = req.user
                    )
                form.save()
                movimiento.save()
                messages.success(req, f'Se actualizó el activo "{activo.nombre}" correctamente.')
                return redirect('/activos/')
        except Exception as e:
            messages.error(req, f'No se pudo actualizar el activo. Error: {str(e)}')

    data = {'form': form, 'accion': 'Actualizar', 'descripcion': 'Cambie los atributos del activo que desea actualizar.'}
    return render(req, 'activo/add_activo.html', data)

@login_required
def del_activo(req, id):
    if req.user.is_superuser:
        activo = Activo.objects.get(id=id)
        activo_bodega = Activo_bodega.objects.filter(activo=activo)
        try:
            #borrar todos los movimientos donde este activo_bodega
            for ab in activo_bodega:
                movimiento = Movimiento.objects.filter(activo_bodega=ab)
                movimiento.delete()
            #borrar todos los activos_bodega donde este activo
            activo_bodega.delete()
            activo.delete()
            messages.success(req, f'Se elimino el activo "{activo.nombre}" correctamente.')
        except Exception as e:
            messages.error(req, f'No se pudo eliminar el activo. Error: {str(e)}')
        return redirect('/activos/')
    else:
        messages.error(req, f'Solamente los super usuarios pueden eliminar un activo.')
        return redirect('/activos/')
#                                                     #
#######################################################

######################## Bodega #######################
#                                                     #
@login_required
def read_bodega(req):
    user = req.user
    bodegas = Bodega.objects.all()
    data = {'bodegas': bodegas, 'user': user}
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
                messages.success(req, f'Se actualizó la bodega "{bodega.nombre}" correctamente.')
                return redirect(f'/bodega/{id}/')
        except Exception as e:
            messages.error(req, f'No se pudo actualizar la bodega. Error: {str(e)}')

    data = {'form': form, 'accion': 'Actualizar', 'descripcion': 'Cambie los atribulos de la bodega que desea actualizar.'}
    return render(req, 'bodega/add_bodega.html', data)

@login_required
def del_bodega(req, id):
    if req.user.is_superuser:
        bodega = Bodega.objects.get(id=id)
        if bodega.nombre == "Sin bodega":
            messages.error(req, f'No se puede eliminar la bodega "{bodega.nombre}".')
            return redirect('/bodegas/')
        try:
            #borrar todos los activos_bodega donde este bodega
            activo_bodega = Activo_bodega.objects.filter(bodega=bodega)
            for ab in activo_bodega:
                movimiento = Movimiento.objects.filter(activo_bodega=ab)
                movimiento.delete()
            activo_bodega.delete()
            bodega.delete()
            messages.success(req, f'Se elimino la bodega "{bodega.nombre}" correctamente.')
        except Exception as e:
            messages.error(req, f'No se pudo eliminar la bodega. Error: {str(e)}')
        return redirect('/bodegas/')
    else:
        messages.error(req, f'Solamente los super usuarios pueden eliminar una bodega.')
        return redirect(f'/bodega/{id}')
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
                tipo_activo = Tipo_activo.objects.last()
                print(tipo_activo)
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
                return redirect('/tipos-de-activos/')
            messages.success(req, f'Se actualizó el tipo de activo "{tipo_activo.nombre}" correctamente.')
        except Exception as e:
            messages.error(req, f'No se pudo actualizar el tipo de activo. Error: {str(e)}')

    data = {'form': form, 'accion': 'Actualizar', 'descripcion': 'Cambie los atribulos del tipo de activo que desea actualizar.'}
    return render(req, 'tipo_activo/add_tipo_activo.html', data)

@login_required
def del_tipo_activo(req, id):
    if req.user.is_superuser:
        tipo_activo = Tipo_activo.objects.get(id=id)
        #comprobar que el tipo de activo no este en ningun activo
        activos = Activo.objects.filter(tipo_activo=tipo_activo)
        if activos.count() > 0:
            messages.error(req, f'No se puede eliminar el tipo de activo "{tipo_activo.nombre}" porque hay activos que lo usan.')
            return redirect('/tipos-de-activos/')
        try:
            tipo_activo.delete()
            messages.success(req, f'Se elimino el tipo de activo "{tipo_activo.nombre}" correctamente.')
        except Exception as e:
            messages.error(req, f'No se pudo eliminar el tipo de activo. Error: {str(e)}')
        return redirect('/tipos-de-activos/')
    else:
        messages.error(req, f'Solamente los super usuarios pueden eliminar un tipo de activo.')
        return redirect('/tipos-de-activos/')
#                                                     #
#######################################################

#################### Activo Bodega ####################
#                                                     #
@login_required
def read_activo_bodega(req, id):
    bodega = Bodega.objects.get(id=id)
    activos = Activo.objects.filter(activo_bodega__bodega=id, activo_bodega__estado=True)
    activos_all = Activo.objects.all()
    if activos_all.count() == 0:
        messages.error(req, f'No se puede agregar activos a la bodega sin activos registrados. Por favor, agregue un activo.')
    data = {'bodega': bodega, 'activos': activos, 'activos_all': activos_all}
    return render(req, 'activo_bodega/read_activo_bodega.html', data)

@login_required
def add_activo_bodega(req, id):
    bodega = Bodega.objects.get(id=id)
    activos = Activo.objects.all()
    activo_bodega = Activo_bodega.objects.all()

    if req.method == 'POST':
        try:
            activos_seleccionados = req.POST.getlist('activo_seleccionado')
            for activo_id in activos_seleccionados:
                activo_actual = Activo.objects.get(id=activo_id)
                activo_bodega_actual = Activo_bodega.objects.filter(activo=activo_actual)
                for ab in activo_bodega_actual:
                    ab.estado = False
                    ab.save()
            
                nuevo_activo_bodega = Activo_bodega(
                    estado = True,
                    activo = activo_actual,
                    bodega = bodega
                )
                nuevo_activo_bodega.save()
            
                movimiento = Movimiento(
                    fecha=datetime.now(),
                    tipo_movimiento = 'AD',
                    cantidad        = activo_actual.cantidad,
                    activo_bodega   = nuevo_activo_bodega,
                    user            = req.user
                )
                movimiento.save()
            return redirect(f'/bodega/{id}/')
        except Exception as e:
            messages.error(req, f'No se pudo mover el activo. Error: {str(e)}')
    
    data = {'bodega': bodega, 'activos': activos, 'activo_bodega': activo_bodega}
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
            activo_bodega = Activo_bodega.objects.filter(activo=activo)
            for ab in activo_bodega:
               ab.estado = False
               ab.save()

            activo_bodega = Activo_bodega(
                estado = True,
                activo = activo,
                bodega = bodega_selecionada
            )
            activo_bodega.save()
            if bodega.nombre == 'Sin bodega':
                movimiento = Movimiento(
                    fecha           = datetime.now(),
                    tipo_movimiento = 'AD',
                    cantidad        = activo.cantidad,
                    activo_bodega   = activo_bodega,
                    user            = req.user
                )
            else:
                movimiento = Movimiento(
                    fecha           = datetime.now(),
                    tipo_movimiento = 'ED',
                    cantidad        = activo.cantidad,
                    activo_bodega   = activo_bodega,
                    user            = req.user
                )
            movimiento.save()
            return redirect(f'/bodega/{id_bodega_selecionada}/')
        except Exception as e:
            messages.error(req, f'No se pudo mover el activo. Error: {str(e)}')
    
    data = {'bodegas': bodegas, 'activo': activo, 'bodega': bodega}
    return render(req, 'activo_bodega/edit_activo_bodega.html', data)

@login_required
def del_activo_bodega(req, id_activo):
    #solamente pone el activo en la bodega "Sin bodega", y pone un registro en movimiento de ello
    activo = Activo.objects.get(id=id_activo)
    activo_bodega = Activo_bodega.objects.filter(activo=activo)
    for ab in activo_bodega:
        ab.estado = False
        ab.save()
    activo_bodega = Activo_bodega(
        estado = True,
        activo = activo,
        bodega = Bodega.objects.get(nombre='Sin bodega')
    )
    activo_bodega.save()
    movimiento = Movimiento(
        fecha           = datetime.now(),
        tipo_movimiento = 'DE',
        cantidad        = activo.cantidad,
        activo_bodega   = activo_bodega,
        user            = req.user
    )
    movimiento.save()
    sin_bodega = Bodega.objects.get(nombre='Sin bodega')
    return redirect(f'/bodega/{sin_bodega.id}/')
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
        if m.tipo_movimiento == 'SB':
            tipo_movimiento = 'Se agrego un activo pero sin bodega'
        elif m.tipo_movimiento == 'AD':
            tipo_movimiento = 'Se agrego un activo a una bodega'
        elif m.tipo_movimiento == 'ED':
            tipo_movimiento = 'Se movio un activo de una bodega a otra bodega'
        elif m.tipo_movimiento == 'DE':
            tipo_movimiento = 'Se quito un activo de una bodega'
        else:
            tipo_movimiento = 'Desconocido'
        cantidad = m.cantidad

        fecha = m.fecha.strftime("%d/%m/%Y %H:%M:%S")
        # Añade un párrafo al PDF
        texto = f'Fecha: {fecha} | Tipo de movimiento: {tipo_movimiento} | Cantidad: {cantidad} | Nombre del activo: {m.activo_bodega.activo.nombre} | Nombre de la bodega: {m.activo_bodega.bodega.nombre} | Usuario: {m.user.username}'
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
