"""
URL configuration for webProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appProject import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signin, name='signin'),
    path('sigout/', views.singout, name='singout'),
    path('inicio/', views.inicio, name='inicio'),

    path('activos/', views.read_activo, name='read_activo'),
    path('agregar-activo/', views.add_activo, name='add_activo'),
    path('actualizar-activo/<int:id>/', views.edit_activo, name='edit_activo'),
    path('eliminar-activo/<int:id>/', views.del_activo, name='del_activo'),

    path('bodegas/', views.read_bodega, name='read_bodega'),
    path('agregar-bodega/', views.add_bodega, name='add_bodega'),
    path('actualizar-bodega/<int:id>/', views.edit_bodega, name='edit_bodega'),
    path('eliminar-bodega/<int:id>/', views.del_bodega, name='del_bodega'),

    path('tipos-de-activos/', views.read_tipo_activo, name='read_tipo_activo'),
    path('agregar-tipo-de-activo/', views.read_tipo_activo, name='add_tipo_activo'),
    path('actualizar-tipo-de-activo/<int:id>/', views.edit_tipo_activo, name='edit_tipo_activo'),
    path('eliminar-tipo-de-activo/<int:id>/', views.del_tipo_activo, name='del_tipo_activo'),
]
