from django.db import models
from django.conf import settings
# Create your models here.


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    provedor = models.CharField(max_length=100)  # Relacionarlo con Proveedor en el futuro
    destino = models.CharField(max_length=100) # Relcionarlo con Destino
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre

class Paquete(models.Model):
    nombre = models.CharField(max_length=100)
    productos = models.ManyToManyField(Producto, related_name='paquetes')
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Paquete"
        verbose_name_plural = "Paquetes"

    def __str__(self):
        return self.nombre


class MetodoPago(models.Model):
    nombe = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)    

    class Meta:
        verbose_name = "Método de Pago"
        verbose_name_plural = "Métodos de Pago"

    def __str__(self):
        return self.nombe
    
 
class EstadoReserva(models.TextChoices):
    PENDIENTE = 'Pendiente', 'Pendiente'
    CONFIRMADA = 'Confirmada', 'Confirmada'
    CANCELADA = 'Cancelada', 'Cancelada'
    COMPLETADA = 'Completada', 'Completada'

    class Meta:
        verbose_name = "Estado de Reserva"
        verbose_name_plural = "Estados de Reserva"

    def __str__(self):
        return self.label






class Reserva(models.Model):
    cliente = models.ForeignKey(core.cliente, on_delete=models.CASCADE)#Relacion con cliente
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)#Relacion con paquete
    empleado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas_atendidas') #Relacion con Empleado
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True)

    estado = models.CharField(max_length=50, choices=EstadoReserva.choices, default=EstadoReserva.PENDIENTE)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente.username} - {self.paquete.nombre}"



class TipoInteraccion(models.TextChoices):
    LLAMADA = 'Llamada', 'Llamada'
    EMAIL = 'Email', 'Email'
    REUNION = 'Reunión', 'Reunión'

    class Meta:
        verbose_name = "Tipo de Interacción"
        verbose_name_plural = "Tipos de Interacción"
    
    def __str__(self):
        return self.label



class Interaccion(models.Model):
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interacciones') #Relacion con cliente
    empleado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interacciones_realizadas') #Relacion con empleado
    tipo = models.CharField(max_length=50, choices=TipoInteraccion.choices, default=TipoInteraccion.LLAMADA) 
    fecha = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Interacción"
        verbose_name_plural = "Interacciones"

    def __str__(self):
        return f"Interacción {self.id} - {self.cliente.username} - {self.tipo}"
    


