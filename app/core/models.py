from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(verbose_name="Email", max_length=254, unique=True)
    telefono_validator = RegexValidator(
        regex=r"^\d{10}$", message="El teléfono debe tener 10 dígitos"
    )
    telefono = models.CharField(
        max_length=10, validators=[telefono_validator], blank=True, null=True
    )
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    preferencias = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nombre}"


class Cargo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def __str__(self):
        return self.nombre


class EmpleadoManager(BaseUserManager):
    def create_user(self, email, nombre, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(email, nombre, password, **extra_fields)


class Empleado(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    telefono_validator = RegexValidator(
        regex=r"^\d{10}$", message="El teléfono debe tener 10 dígitos"
    )
    phone = models.CharField(max_length=10, validators=[telefono_validator], blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    imagen = models.ImageField(upload_to="empleados/", blank=True, null=True)
    cover = models.ImageField(upload_to="empleados/covers/", blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    puesto = models.ForeignKey(
        Cargo, on_delete=models.SET_NULL, blank=True, null=True
    )  # Cargo en la agencia (Vendedor/Gerente)
    date_joined = models.DateField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    fecha_contratacion = models.DateField(default=timezone.now)

    objects = EmpleadoManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre"]

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
        puesto = self.puesto.nombre if self.puesto else "Sin puesto"
        return f"{self.nombre} - {puesto}"


class Proveedor(models.Model):
    TIPO_CHOICES = [
        ("Aerolínea", "Aerolínea"),
        ("Hotel", "Hotel"),
        ("Transporte", "Transporte"),
        ("Otro", "Otro"),
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    contacto = models.CharField(unique=True, max_length=100)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Destino(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Destino"
        verbose_name_plural = "Destinos"
        ordering = ["pais", "nombre"]
        unique_together = [("nombre", "pais")]

    def __str__(self):
        return f"{self.nombre}, {self.pais}"


class Producto(models.Model):
    TIPO_CHOICES = [
        ("Vuelo", "Vuelo"),
        ("Hotel", "Hotel"),
        ("Tour", "Tour"),
        ("Otro", "Otro"),
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, related_name="productos", null=True
    )
    destino = models.ForeignKey(
        Destino, on_delete=models.CASCADE, related_name="productos", null=True
    )
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["tipo", "nombre"]

    def __str__(self):
        return self.nombre


class Paquete(models.Model):
    nombre = models.CharField(max_length=100)
    productos = models.ManyToManyField(Producto, related_name="paquetes")
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Paquete"
        verbose_name_plural = "Paquetes"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class MetodoPago(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Método de Pago"
        verbose_name_plural = "Métodos de Pago"

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)
    empleado = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservas_atendidas"
    )
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True)

    ESTADO_CHOICES = [
        ("Pendiente", "Pendiente"),
        ("Confirmada", "Confirmada"),
        ("Cancelada", "Cancelada"),
        ("Completada", "Completada"),
    ]
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default="Pendiente")

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente.nombre} - {self.paquete.nombre}"


class TipoInteraccion(models.TextChoices):
    LLAMADA = "Llamada", "Llamada"
    EMAIL = "Email", "Email"
    REUNION = "Reunión", "Reunión"

    class Meta:
        verbose_name = "Tipo de Interacción"
        verbose_name_plural = "Tipos de Interacción"

    def __str__(self):
        return self.label


class Interaccion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="interacciones")
    empleado = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interacciones_realizadas"
    )
    tipo = models.CharField(max_length=50, choices=TipoInteraccion.choices, default=TipoInteraccion.LLAMADA)
    fecha = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Interacción"
        verbose_name_plural = "Interacciones"
        ordering = ["-fecha"]

    def __str__(self):
        return f"Interacción {self.id} - {self.cliente.nombre} - {self.tipo}"

