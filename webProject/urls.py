from django.contrib import admin
from django.urls import path
from appProject import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signin, name='signin'),
    path('sigout/', views.singout, name='singout'),
    path('inicio/', views.inicio, name='inicio'),
    path('movimientos/', views.read_movimiento, name='read_movimiento'),
    path('generar-informe/', views.generar_pdf, name='generar_pdf'),

    path('activos/', views.read_activo, name='read_activo'),
    path('agregar-activo/', views.add_activo, name='add_activo'),
    path('actualizar-activo/<int:id>/', views.edit_activo, name='edit_activo'),
    path('eliminar-activo/<int:id>/', views.del_activo, name='del_activo'),

    path('bodegas/', views.read_bodega, name='read_bodega'),
    path('agregar-bodega/', views.add_bodega, name='add_bodega'),
    path('actualizar-bodega/<int:id>/', views.edit_bodega, name='edit_bodega'),
    path('eliminar-bodega/<int:id>/', views.del_bodega, name='del_bodega'),

    path('tipos-de-activos/', views.read_tipo_activo, name='read_tipo_activo'),
    path('agregar-tipo-de-activo/', views.add_tipo_activo, name='add_tipo_activo'),
    path('actualizar-tipo-de-activo/<int:id>/', views.edit_tipo_activo, name='edit_tipo_activo'),
    path('eliminar-tipo-de-activo/<int:id>/', views.del_tipo_activo, name='del_tipo_activo'),

    path('bodega/<int:id>/', views.read_activo_bodega, name='read_activo_bodega'),
    path('agregar-activo-bodega/<int:id>/', views.add_activo_bodega, name='add_activo_bodega'),
    path('mover-activo-bodega/<int:id_bodega>/<int:id_activo>/', views.edit_activo_bodega, name='edit_activo_bodega'),
    path('quitar-activo-bodega/<int:id_bodega>/<int:id_activo>/', views.del_activo_bodega, name='del_activo_bodega'),
]
