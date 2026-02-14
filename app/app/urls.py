# app/app/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from core.auth_forms import EmailAuthenticationForm
from core import views

# ====== PATTERNS POR MODULO (TODO EN CORE) ======

clientes_patterns = ([
    path("", views.ClienteListView.as_view(), name="cliente_list"),
    path("nuevo/", views.ClienteCreateView.as_view(), name="cliente_create"),
    path("<int:pk>/editar/", views.ClienteUpdateView.as_view(), name="cliente_update"),
    path("<int:pk>/eliminar/", views.ClienteDeleteView.as_view(), name="cliente_delete"),
], "clientes")

paquetes_patterns = ([
    path("", views.PaqueteListView.as_view(), name="paquete_list"),
    path("nuevo/", views.PaqueteCreateView.as_view(), name="paquete_create"),
    path("<int:pk>/", views.PaqueteDetailView.as_view(), name="paquete_detail"),
    path("<int:pk>/editar/", views.PaqueteUpdateView.as_view(), name="paquete_update"),
    path("<int:pk>/eliminar/", views.PaqueteDeleteView.as_view(), name="paquete_delete"),
], "paquetes")

productos_patterns = ([
    path("", views.ProductoListView.as_view(), name="producto_list"),
    path("nuevo/", views.ProductoCreateView.as_view(), name="producto_create"),
    path("<int:pk>/editar/", views.ProductoUpdateView.as_view(), name="producto_update"),
    path("<int:pk>/eliminar/", views.ProductoDeleteView.as_view(), name="producto_delete"),
], "productos")

proveedores_patterns = ([
    path("", views.ProveedorListView.as_view(), name="proveedor_list"),
    path("nuevo/", views.ProveedorCreateView.as_view(), name="proveedor_create"),
    path("<int:pk>/editar/", views.ProveedorUpdateView.as_view(), name="proveedor_update"),
    path("<int:pk>/eliminar/", views.ProveedorDeleteView.as_view(), name="proveedor_delete"),
], "proveedores")

destinos_patterns = ([
    path("", views.DestinoListView.as_view(), name="destino_list"),
    path("nuevo/", views.DestinoCreateView.as_view(), name="destino_create"),
    path("<int:pk>/editar/", views.DestinoUpdateView.as_view(), name="destino_update"),
    path("<int:pk>/eliminar/", views.DestinoDeleteView.as_view(), name="destino_delete"),
], "destinos")

reservas_patterns = ([
    path("", views.ReservaListView.as_view(), name="reserva_list"),
    path("nuevo/", views.ReservaCreateView.as_view(), name="reserva_create"),
    path("<int:pk>/editar/", views.ReservaUpdateView.as_view(), name="reserva_update"),
    path("<int:pk>/eliminar/", views.ReservaDeleteView.as_view(), name="reserva_delete"),
], "reservas")

interacciones_patterns = ([
    path("", views.InteraccionListView.as_view(), name="interaccion_list"),
    path("nuevo/", views.InteraccionCreateView.as_view(), name="interaccion_create"),
    path("<int:pk>/editar/", views.InteraccionUpdateView.as_view(), name="interaccion_update"),
    path("<int:pk>/eliminar/", views.InteraccionDeleteView.as_view(), name="interaccion_delete"),
], "interacciones")

metodopago_patterns = ([
    path("", views.MetodoPagoListView.as_view(), name="metodopago_list"),
    path("nuevo/", views.MetodoPagoCreateView.as_view(), name="metodopago_create"),
    path("<int:pk>/editar/", views.MetodoPagoUpdateView.as_view(), name="metodopago_update"),
    path("<int:pk>/eliminar/", views.MetodoPagoDeleteView.as_view(), name="metodopago_delete"),
], "metodopago")

roles_patterns = ([
    path("", views.RolListView.as_view(), name="rol_list"),
    path("nuevo/", views.RolCreateView.as_view(), name="rol_create"),
    path("<int:pk>/editar/", views.RolUpdateView.as_view(), name="rol_update"),
    path("<int:pk>/eliminar/", views.RolDeleteView.as_view(), name="rol_delete"),
], "roles")

colaboradores_patterns = ([
    path("", views.EmpleadoListView.as_view(), name="empleado_list"),
    path("nuevo/", views.EmpleadoCreateView.as_view(), name="empleado_create"),
    path("<int:pk>/editar/", views.EmpleadoUpdateView.as_view(), name="empleado_update"),
    path("<int:pk>/eliminar/", views.EmpleadoDeleteView.as_view(), name="empleado_delete"),
], "colaboradores")


urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ Raíz => si no está logueado manda a login
    path("", views.RootRedirectView.as_view(), name="root"),

    # Tu dashboard
    path("inicio/", views.IndexView.as_view(), name="home"),


    # Auth
    path("login/", auth_views.LoginView.as_view(
        template_name="auth/login.html",
        authentication_form=EmailAuthenticationForm,
        redirect_authenticated_user=True,
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),


    # Error acceso
    path("403/", views.AccessDeniedView.as_view(), name="access_denied"),

    # Módulos
    path("clientes/", include(clientes_patterns, namespace="clientes")),
    path("paquetes/", include(paquetes_patterns, namespace="paquetes")),
    path("productos/", include(productos_patterns, namespace="productos")),
    path("proveedores/", include(proveedores_patterns, namespace="proveedores")),
    path("destinos/", include(destinos_patterns, namespace="destinos")),
    path("reservas/", include(reservas_patterns, namespace="reservas")),
    path("interacciones/", include(interacciones_patterns, namespace="interacciones")),
    path("metodos-pago/", include(metodopago_patterns, namespace="metodopago")),

    # Fase 2 (UI)
    path("roles/", include(roles_patterns, namespace="roles")),
    path("colaboradores/", include(colaboradores_patterns, namespace="colaboradores")),
]
