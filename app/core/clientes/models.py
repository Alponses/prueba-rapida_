from django.db import models
from django.conf import settings

# Create your models here.



class Empleado (models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    imagen = models.ImageField(upload_to='empleados/', blank=True, null=True)
    cover = models.ImageField(upload_to='empleados/covers/', blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    puesto = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.puesto}"


    



