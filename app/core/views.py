from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from django.views.generic import TemplateView
from core.mixins import PermissionRedirectMixin
from .models import Cliente, Destino, Interaccion, MetodoPago, Paquete, Producto, Proveedor, Reserva

from .forms import (
    ClienteForm,
    DestinoForm,
    InteraccionForm,
    MetodoPagoForm,
    PaqueteForm,
    ProductoForm,
    ProveedorForm,
    ReservaForm,
)
from .models import (
    Cliente,
    Destino,
    Interaccion,
    MetodoPago,
    Paquete,
    Producto,
    Proveedor,
    Reserva,
)


class IndexView(TemplateView):
    template_name = 'index.html'



# core/clientes/views.py

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd["username"],
                                password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Autenticación exitosa.")
                else:
                    messages.error(request, "Cuenta deshabilitada.")
            else:
                return HttpResponse("Datos de autenticación inválidos.")
        else:
            form = LoginForm()
        return render(request, "login.html", {"form": form})



class ClienteListView(PermissionRedirectMixin,ListView):
    required_perm = "core.view_cliente"
    model = Cliente
    template_name = "clientes/clientes_list.html"
    context_object_name = "clientes"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) |
                Q(email__icontains=q) |
                Q(preferencias__icontains=q)
            )
        return qs

class ClienteCreateView(PermissionRedirectMixin,CreateView):
    required_perm = "core.add_cliente"
    model = Cliente
    form_class = ClienteForm
    template_name = "create.html"
    success_url = reverse_lazy("clientes:cliente_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Nuevo Cliente",
                "submit_label": "Crear cliente",
                "cancel_url": reverse_lazy("clientes:cliente_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Cliente creado correctamente.")
        return super().form_valid(form)

class ClienteUpdateView(PermissionRedirectMixin, UpdateView):
    required_perm = "core.change_cliente"
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_update.html"
    success_url = reverse_lazy("clientes:cliente_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Editar Cliente",
                "submit_label": "Guardar cambios",
                "cancel_url": reverse_lazy("clientes:cliente_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Cliente actualizado.")
        return super().form_valid(form)



class ClienteDeleteView(PermissionRedirectMixin, DeleteView):
    required_perm = "core.delete_cliente"
    model = Cliente
    success_url = reverse_lazy("clientes:cliente_list")

    def get(self, request, *args, **kwargs):
        # Eliminar directamente en GET (sin plantilla de confirmación)
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        nombre = getattr(obj, "nombre", str(obj))
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Cliente {nombre} eliminado correctamente.")
        return response



class PaqueteListView(PermissionRedirectMixin,ListView):
    required_perm = "core.view_paquete"
    model = Paquete
    template_name = "paquetes/paquete_list.html"
    context_object_name = "paquetes"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("productos__proveedor", "productos__destino")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q)
                | Q(productos__nombre__icontains=q)
                | Q(productos__destino__nombre__icontains=q)
            ).distinct()
        return qs
    
class PaqueteCreateView(PermissionRedirectMixin, CreateView):
    # Implementación similar a ClienteCreateView
    required_perm = "core.add_paquete"
    model = Paquete
    form_class = PaqueteForm
    template_name = "create.html"
    success_url = reverse_lazy("paquetes:paquete_list")
    require_permission = "core.add_paquete"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Nuevo Paquete",
                "submit_label": "Crear paquete",
                "cancel_url": reverse_lazy("paquetes:paquete_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Paquete creado correctamente.")
        return super().form_valid(form)
    
class PaqueteUpdateView(PermissionRedirectMixin, UpdateView):
    # Implementación similar a ClienteUpdateView
    required_perm = "core.change_paquete"
    model = Paquete
    form_class = PaqueteForm
    template_name = "paquetes/paquete_update.html"
    success_url = reverse_lazy("paquetes:paquete_list")
    require_permission = "core.change_paquete"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Editar Paquete",
                "submit_label": "Guardar cambios",
                "cancel_url": reverse_lazy("paquetes:paquete_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Paquete actualizado.")
        return super().form_valid(form) 
    
class PaqueteDeleteView(PermissionRedirectMixin, DeleteView):
    # Implementación similar a ClienteDeleteView
    required_perm = "core.delete_paquete"
    model = Paquete
    success_url = reverse_lazy("paquetes:paquete_list")
    require_permission = "core.delete_paquete"

    def get(self, request, *args, **kwargs):
        # Eliminar directamente en GET (sin plantilla de confirmación)
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        nombre = getattr(obj, "nombre", str(obj))
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Paquete {nombre} eliminado correctamente.")
        return response


# Productos
class ProductoListView(PermissionRedirectMixin,ListView):
    required_perm = "core.view_producto"
    model = Producto
    template_name = "paquetes/productos/productos_list.html"
    context_object_name = "productos"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("proveedor", "destino")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q)
                | Q(tipo__icontains=q)
                | Q(proveedor__nombre__icontains=q)
                | Q(destino__nombre__icontains=q)
                | Q(destino__pais__icontains=q)
            )
        return qs


class ProductoCreateView(PermissionRedirectMixin, CreateView):
    required_perm = "core.add_producto"
    model = Producto
    form_class = ProductoForm
    template_name = "create.html"
    success_url = reverse_lazy("productos:producto_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Nuevo Producto",
                "submit_label": "Crear producto",
                "cancel_url": reverse_lazy("productos:producto_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Producto creado correctamente.")
        return super().form_valid(form)


class ProductoUpdateView(PermissionRedirectMixin, UpdateView):
    required_perm = "core.change_producto"
    model = Producto
    form_class = ProductoForm
    template_name = "paquetes/productos/producto_update.html"
    success_url = reverse_lazy("productos:producto_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Editar Producto",
                "submit_label": "Guardar cambios",
                "cancel_url": reverse_lazy("productos:producto_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado.")
        return super().form_valid(form)


class ProductoDeleteView(PermissionRedirectMixin, DeleteView):
    required_perm = "core.delete_producto"
    model = Producto
    success_url = reverse_lazy("productos:producto_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        nombre = getattr(obj, "nombre", str(obj))
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Producto {nombre} eliminado correctamente.")
        return response


class ProveedorListView(PermissionRedirectMixin, ListView):
    required_perm = "core.view_proveedor"
    model = Proveedor
    template_name = "proveedores/proveedor_list.html"
    context_object_name = "proveedores"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q)
                | Q(tipo__icontains=q)
                | Q(contacto__icontains=q)
            )
        return qs


class ProveedorCreateView(PermissionRedirectMixin, CreateView):
    required_perm = "core.add_proveedor"
    model = Proveedor
    form_class = ProveedorForm
    template_name = "create.html"
    success_url = reverse_lazy("proveedores:proveedor_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Nuevo Proveedor",
                "submit_label": "Crear proveedor",
                "cancel_url": reverse_lazy("proveedores:proveedor_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Proveedor creado correctamente.")
        return super().form_valid(form)


class ProveedorUpdateView(PermissionRedirectMixin, UpdateView):
    required_perm = "core.change_proveedor"
    model = Proveedor
    form_class = ProveedorForm
    template_name = "proveedores/proveedor_update.html"
    success_url = reverse_lazy("proveedores:proveedor_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Editar Proveedor",
                "submit_label": "Guardar cambios",
                "cancel_url": reverse_lazy("proveedores:proveedor_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Proveedor actualizado.")
        return super().form_valid(form)


class ProveedorDeleteView(PermissionRedirectMixin, DeleteView):
    required_perm = "core.delete_proveedor"
    model = Proveedor
    success_url = reverse_lazy("proveedores:proveedor_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        nombre = getattr(obj, "nombre", str(obj))
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Proveedor {nombre} eliminado correctamente.")
        return response


class DestinoListView(PermissionRedirectMixin, ListView):
    required_perm = "core.view_destino"
    model = Destino
    template_name = "destinos/destino_list.html"
    context_object_name = "destinos"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q)
                | Q(pais__icontains=q)
                | Q(descripcion__icontains=q)
            )
        return qs


class DestinoCreateView(PermissionRedirectMixin, CreateView):
    required_perm = "core.add_destino"
    model = Destino
    form_class = DestinoForm
    template_name = "create.html"
    success_url = reverse_lazy("destinos:destino_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Nuevo Destino",
                "submit_label": "Crear destino",
                "cancel_url": reverse_lazy("destinos:destino_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Destino creado correctamente.")
        return super().form_valid(form)


class DestinoUpdateView(PermissionRedirectMixin, UpdateView):
    required_perm = "core.change_destino"
    model = Destino
    form_class = DestinoForm
    template_name = "destinos/destino_update.html"
    success_url = reverse_lazy("destinos:destino_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Editar Destino",
                "submit_label": "Guardar cambios",
                "cancel_url": reverse_lazy("destinos:destino_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Destino actualizado.")
        return super().form_valid(form)


class DestinoDeleteView(PermissionRedirectMixin, DeleteView):
    required_perm = "core.delete_destino"
    model = Destino
    success_url = reverse_lazy("destinos:destino_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        nombre = getattr(obj, "nombre", str(obj))
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Destino {nombre} eliminado correctamente.")
        return response


# Métodos de pago
class MetodoPagoListView(PermissionRedirectMixin, ListView):
    required_perm = "core.view_metodopago"
    model = MetodoPago
    template_name = "paquetes/metodoDePago/metodo_list.html"
    context_object_name = "metodos"


class MetodoPagoCreateView(PermissionRedirectMixin, CreateView):
    required_perm = "core.add_metodopago"
    model = MetodoPago
    form_class = MetodoPagoForm
    template_name = "create.html"
    success_url = reverse_lazy("metodopago:metodopago_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Nuevo Método de Pago",
                "submit_label": "Crear método",
                "cancel_url": reverse_lazy("metodopago:metodopago_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Método de pago creado correctamente.")
        return super().form_valid(form)


class MetodoPagoUpdateView(PermissionRedirectMixin, UpdateView):
    required_perm = "core.change_metodopago"
    model = MetodoPago
    form_class = MetodoPagoForm
    template_name = "paquetes/metodoDePago/metodo_update.html"
    success_url = reverse_lazy("metodopago:metodopago_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Editar Método de Pago",
                "submit_label": "Guardar cambios",
                "cancel_url": reverse_lazy("metodopago:metodopago_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Método de pago actualizado.")
        return super().form_valid(form)


class MetodoPagoDeleteView(PermissionRedirectMixin, DeleteView):
    required_perm = "core.delete_metodopago"
    model = MetodoPago
    success_url = reverse_lazy("metodopago:metodopago_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        nombre = getattr(obj, "nombre", str(obj))
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Método de pago {nombre} eliminado correctamente.")
        return response


class ReservaListView(PermissionRedirectMixin, ListView):
    required_perm = "core.view_reserva"
    model = Reserva
    template_name = "reservas/reserva_list.html"
    context_object_name = "reservas"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("cliente", "paquete", "empleado", "metodo_pago")
        )
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(cliente__nombre__icontains=q)
                | Q(paquete__nombre__icontains=q)
                | Q(empleado__nombre__icontains=q)
                | Q(estado__icontains=q)
            )
        return qs


class ReservaCreateView(PermissionRedirectMixin, CreateView):
    required_perm = "core.add_reserva"
    model = Reserva
    form_class = ReservaForm
    template_name = "create.html"
    success_url = reverse_lazy("reservas:reserva_list")

    def form_valid(self, form):
        form.instance.empleado = self.request.user
        if not form.instance.precio_venta and form.instance.paquete:
            form.instance.precio_venta = form.instance.paquete.precio_final
            messages.success(self.request, "Reserva creada correctamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Nueva Reserva",
                "submit_label": "Crear reserva",
                "cancel_url": reverse_lazy("reservas:reserva_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Reserva creada correctamente.")
        return super().form_valid(form)


class ReservaUpdateView(PermissionRedirectMixin, UpdateView):
    required_perm = "core.change_reserva"
    model = Reserva
    form_class = ReservaForm
    template_name = "reservas/reserva_update.html"
    success_url = reverse_lazy("reservas:reserva_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Editar Reserva",
                "submit_label": "Guardar cambios",
                "cancel_url": reverse_lazy("reservas:reserva_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Reserva actualizada.")
        return super().form_valid(form)


class ReservaDeleteView(PermissionRedirectMixin, DeleteView):
    required_perm = "core.delete_reserva"
    model = Reserva
    success_url = reverse_lazy("reservas:reserva_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Reserva {obj.id} eliminada correctamente.")
        return response


class InteraccionListView(PermissionRedirectMixin, ListView):
    required_perm = "core.view_interaccion"
    model = Interaccion
    template_name = "interacciones/interaccion_list.html"
    context_object_name = "interacciones"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("cliente", "empleado")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(cliente__nombre__icontains=q)
                | Q(empleado__nombre__icontains=q)
                | Q(tipo__icontains=q)
                | Q(notas__icontains=q)
            )
        return qs


class InteraccionCreateView(PermissionRedirectMixin, CreateView):
    required_perm = "core.add_interaccion"
    model = Interaccion
    form_class = InteraccionForm
    template_name = "create.html"
    success_url = reverse_lazy("interacciones:interaccion_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Nueva Interacción",
                "submit_label": "Registrar interacción",
                "cancel_url": reverse_lazy("interacciones:interaccion_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Interacción registrada correctamente.")
        return super().form_valid(form)


class InteraccionUpdateView(PermissionRedirectMixin, UpdateView):
    required_perm = "core.change_interaccion"
    model = Interaccion
    form_class = InteraccionForm
    template_name = "interacciones/interaccion_update.html"
    success_url = reverse_lazy("interacciones:interaccion_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "page_title": "Editar Interacción",
                "submit_label": "Guardar cambios",
                "cancel_url": reverse_lazy("interacciones:interaccion_list"),
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Interacción actualizada.")
        return super().form_valid(form)


class InteraccionDeleteView(PermissionRedirectMixin, DeleteView):
    required_perm = "core.delete_interaccion"
    model = Interaccion
    success_url = reverse_lazy("interacciones:interaccion_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Interacción {obj.id} eliminada correctamente.")
        return response









class AccessDeniedView(TemplateView):
    template_name = "errors/403.html"
