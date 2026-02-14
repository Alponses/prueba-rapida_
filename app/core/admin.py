from django.contrib import admin

from .models import (
    Cargo,
    Cliente,
    Destino,
    Empleado,
    Interaccion,
    MetodoPago,
    Paquete,
    Producto,
    Proveedor,
    Reserva,
    Comentario,

)



@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "telefono", "fecha_registro")
    search_fields = ("nombre", "email")


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "contacto")
    search_fields = ("nombre", "contacto")
    list_filter = ("tipo",)


@admin.register(Destino)
class DestinoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "pais")
    search_fields = ("nombre", "pais")
    list_filter = ("pais",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "proveedor", "destino", "precio_base")
    list_filter = ("tipo", "proveedor", "destino")
    search_fields = ("nombre",)


@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio_final", "activo")
    list_filter = ("activo",)
    filter_horizontal = ("productos",)


@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ("nombre",)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "paquete", "empleado", "estado", "fecha_reserva")
    list_filter = ("estado", "fecha_reserva")
    search_fields = ("cliente__nombre", "paquete__nombre")


@admin.register(Interaccion)
class InteraccionAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "empleado", "tipo", "fecha")
    list_filter = ("tipo", "fecha")
    search_fields = ("cliente__nombre", "empleado__nombre", "notas")


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("nombre",)


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("email", "nombre", "puesto", "is_active", "is_staff")
    search_fields = ("email", "nombre")

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("paquete", "autor", "calificacion", "creado_en")
    list_filter = ("calificacion", "creado_en")
    search_fields = ("paquete__nombre", "autor__email", "autor__nombre", "texto")
