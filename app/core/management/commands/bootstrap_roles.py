from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

# Ajusta estos roles a tu lógica.
# Como tus modelos están en core/models.py, el app_label = "core"
ROLE_PERMS = {
    "Asesor de Ventas": [
        # Clientes (CRUD parcial)
        "core.view_cliente",
        "core.add_cliente",
        "core.change_cliente",

        # Ver catálogo para vender
        "core.view_paquete",
        "core.view_producto",
        "core.view_destino",
        "core.view_proveedor",

        # Reservas (crear + ver)
        "core.view_reserva",
        "core.add_reserva",

        # Interacciones (crear + ver)
        "core.view_interaccion",
        "core.add_interaccion",
    ],
    "Gerente": [
        # Clientes (CRUD completo)
        "core.view_cliente",
        "core.add_cliente",
        "core.change_cliente",
        "core.delete_cliente",

        # Catálogo (administra)
        "core.view_paquete", "core.add_paquete", "core.change_paquete", "core.delete_paquete",
        "core.view_producto", "core.add_producto", "core.change_producto", "core.delete_producto",
        "core.view_destino", "core.add_destino", "core.change_destino", "core.delete_destino",
        "core.view_proveedor", "core.add_proveedor", "core.change_proveedor", "core.delete_proveedor",

        # Reservas (CRUD completo)
        "core.view_reserva",
        "core.add_reserva",
        "core.change_reserva",
        "core.delete_reserva",

        # Métodos de pago
        "core.view_metodopago",
        "core.add_metodopago",
        "core.change_metodopago",
        "core.delete_metodopago",

        # Interacciones (CRUD completo)
        "core.view_interaccion",
        "core.add_interaccion",
        "core.change_interaccion",
        "core.delete_interaccion",
    ],
    "Administrador": [
        # Todo en core (como gerente + empleados/cargos si quieres)
        "core.view_cliente", "core.add_cliente", "core.change_cliente", "core.delete_cliente",
        "core.view_paquete", "core.add_paquete", "core.change_paquete", "core.delete_paquete",
        "core.view_producto", "core.add_producto", "core.change_producto", "core.delete_producto",
        "core.view_destino", "core.add_destino", "core.change_destino", "core.delete_destino",
        "core.view_proveedor", "core.add_proveedor", "core.change_proveedor", "core.delete_proveedor",
        "core.view_reserva", "core.add_reserva", "core.change_reserva", "core.delete_reserva",
        "core.view_metodopago", "core.add_metodopago", "core.change_metodopago", "core.delete_metodopago",
        "core.view_interaccion", "core.add_interaccion", "core.change_interaccion", "core.delete_interaccion",

        # Si quieres que admins gestionen empleados y cargos (opcional):
        "core.view_empleado", "core.add_empleado", "core.change_empleado", "core.delete_empleado",
        "core.view_cargo", "core.add_cargo", "core.change_cargo", "core.delete_cargo",
    ],
}

class Command(BaseCommand):
    help = "Crea/actualiza grupos (roles) y asigna permisos por codename"

    def handle(self, *args, **options):
        missing = []

        for role, perm_codes in ROLE_PERMS.items():
            group, _ = Group.objects.get_or_create(name=role)
            group.permissions.clear()

            for perm_code in perm_codes:
                app_label, codename = perm_code.split(".", 1)
                try:
                    perm = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename
                    )
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    missing.append(perm_code)

            self.stdout.write(self.style.SUCCESS(f"OK -> Grupo '{role}' actualizado."))

        if missing:
            self.stdout.write(self.style.WARNING("\nPermisos NO encontrados (revisa app_label/codename):"))
            for m in sorted(set(missing)):
                self.stdout.write(self.style.WARNING(f" - {m}"))
            self.stdout.write(self.style.WARNING("\nTip: asegúrate de haber corrido migrate y de que los modelos estén en la app correcta."))
