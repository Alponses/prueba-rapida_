"""
URL configuration for app project.

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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views
from core.auth_forms import EmailAuthenticationForm
from core.views import IndexView, AccessDeniedView  





clientes = (
    [
        path("", views.ClienteListView.as_view(), name="cliente_list"),
        path("nuevo/", views.ClienteCreateView.as_view(), name="cliente_create"),
        path("<int:pk>/editar/", views.ClienteUpdateView.as_view(), name="cliente_update"),
        path("<int:pk>/eliminar/", views.ClienteDeleteView.as_view(), name="cliente_delete"),
    ],
    "clientes",
)

paquetes = (
    [
        path("", views.PaqueteListView.as_view(), name="paquete_list"),
        path("nuevo/", views.PaqueteCreateView.as_view(), name="paquete_create"),
        path("<int:pk>/editar/", views.PaqueteUpdateView.as_view(), name="paquete_update"),
        path("<int:pk>/eliminar/", views.PaqueteDeleteView.as_view(), name="paquete_delete"),
    ],
    "paquetes",
)

productos = (
    [
        path("", views.ProductoListView.as_view(), name="producto_list"),
        path("nuevo/", views.ProductoCreateView.as_view(), name="producto_create"),
        path("<int:pk>/editar/", views.ProductoUpdateView.as_view(), name="producto_update"),
        path("<int:pk>/eliminar/", views.ProductoDeleteView.as_view(), name="producto_delete"),
    ],
    "productos",
)

proveedores = (
    [
        path("", views.ProveedorListView.as_view(), name="proveedor_list"),
        path("nuevo/", views.ProveedorCreateView.as_view(), name="proveedor_create"),
        path("<int:pk>/editar/", views.ProveedorUpdateView.as_view(), name="proveedor_update"),
        path("<int:pk>/eliminar/", views.ProveedorDeleteView.as_view(), name="proveedor_delete"),
    ],
    "proveedores",
)

destinos = (
    [
        path("", views.DestinoListView.as_view(), name="destino_list"),
        path("nuevo/", views.DestinoCreateView.as_view(), name="destino_create"),
        path("<int:pk>/editar/", views.DestinoUpdateView.as_view(), name="destino_update"),
        path("<int:pk>/eliminar/", views.DestinoDeleteView.as_view(), name="destino_delete"),
    ],
    "destinos",
)

reservas = (
    [
        path("", views.ReservaListView.as_view(), name="reserva_list"),
        path("nuevo/", views.ReservaCreateView.as_view(), name="reserva_create"),
        path("<int:pk>/editar/", views.ReservaUpdateView.as_view(), name="reserva_update"),
        path("<int:pk>/eliminar/", views.ReservaDeleteView.as_view(), name="reserva_delete"),
    ],
    "reservas",
)

interacciones = (
    [
        path("", views.InteraccionListView.as_view(), name="interaccion_list"),
        path("nuevo/", views.InteraccionCreateView.as_view(), name="interaccion_create"),
        path("<int:pk>/editar/", views.InteraccionUpdateView.as_view(), name="interaccion_update"),
        path("<int:pk>/eliminar/", views.InteraccionDeleteView.as_view(), name="interaccion_delete"),
    ],
    "interacciones",
)

metodopago = (
    [
        path("", views.MetodoPagoListView.as_view(), name="metodopago_list"),
        path("nuevo/", views.MetodoPagoCreateView.as_view(), name="metodopago_create"),
        path("<int:pk>/editar/", views.MetodoPagoUpdateView.as_view(), name="metodopago_update"),
        path("<int:pk>/eliminar/", views.MetodoPagoDeleteView.as_view(), name="metodopago_delete"),
    ],
    "metodopago",
)


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", IndexView.as_view(), name="index"),

    path("login/", auth_views.LoginView.as_view(
        template_name="auth/login.html",
        authentication_form=EmailAuthenticationForm
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("403/", AccessDeniedView.as_view(), name="access_denied"),

    path("clientes/", include(clientes, namespace="clientes")),
    path("paquetes/", include(paquetes, namespace="paquetes")),
    path("productos/", include(productos, namespace="productos")),
    path("proveedores/", include(proveedores, namespace="proveedores")),
    path("destinos/", include(destinos, namespace="destinos")),
    path("reservas/", include(reservas, namespace="reservas")),
    path("interacciones/", include(interacciones, namespace="interacciones")),
    path("metodos-pago/", include(metodopago, namespace="metodopago")),
]
