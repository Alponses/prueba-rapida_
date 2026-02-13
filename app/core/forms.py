from django import forms
from typing import cast
from django.forms import (
    CheckboxSelectMultiple,
    ModelMultipleChoiceField,
    NumberInput,
    Select,
    SelectMultiple,
    TextInput,
    EmailInput,
    Textarea,
)

from .models import (
    Cliente,
    Destino,
    Empleado,
    Interaccion,
    MetodoPago,
    Paquete,
    Producto,
    Proveedor,
    Reserva,
)

from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model


class RolForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related("content_type").all(),
        required=False,
    )

    class Meta:
        model = Group
        fields = ("name", "permissions")
        labels = {"name": "Nombre"}
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "email", "telefono", "preferencias"]
        labels = {
            "nombre": "Nombre",
            "email": "Email",
            "telefono": "Teléfono",
            "preferencias": "Preferencias",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "preferencias": forms.TextInput(attrs={"class": "form-control"}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nombre", "tipo", "contacto"]
        labels = {
            "nombre": "Nombre",
            "tipo": "Tipo de servicio",
            "contacto": "Contacto",
        }
        widgets = {
            "nombre": TextInput(attrs={"class": "form-control"}),
            "tipo": Select(attrs={"class": "form-control"}),
            "contacto": TextInput(attrs={"class": "form-control"}),
        }


class DestinoForm(forms.ModelForm):
    class Meta:
        model = Destino
        fields = ["nombre", "pais", "descripcion"]
        labels = {
            "nombre": "Nombre",
            "pais": "País",
            "descripcion": "Descripción",
        }
        widgets = {
            "nombre": TextInput(attrs={"class": "form-control"}),
            "pais": TextInput(attrs={"class": "form-control"}),
            "descripcion": Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "tipo", "proveedor", "destino", "precio_base"]
        labels = {
            "nombre": "Nombre",
            "tipo": "Tipo",
            "proveedor": "Proveedor",
            "destino": "Destino",
            "precio_base": "Precio base",
        }
        widgets = {
            "nombre": TextInput(attrs={"class": "form-control"}),
            "tipo": Select(attrs={"class": "form-control"}),
            "proveedor": Select(attrs={"class": "form-control"}),
            "destino": Select(attrs={"class": "form-control"}),
            "precio_base": NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.01"}),
        }

    def clean_precio_base(self):
        precio = self.cleaned_data.get("precio_base")
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a cero.")
        return precio


class PaqueteForm(forms.ModelForm):
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        label="Productos incluidos",
        help_text="Seleccione los productos que incluye este paquete.",
    )

    class Meta:
        model = Paquete
        fields = ["nombre", "productos", "precio_final", "activo"]
        labels = {
            "nombre": "Nombre del paquete",
            "precio_final": "Precio final",
            "activo": "Activo",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "precio_final": forms.NumberInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["productos"].queryset = Producto.objects.order_by("nombre")


#   # En un futuro vamos a hacer que tenga choise
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        productos_field = cast(forms.ModelMultipleChoiceField, self.fields["productos"])
#        productos_field.queryset = Producto.objects.select_related("proveedor", "destino").order_by("nombre")
#
    def clean_precio_final(self):
        precio = self.cleaned_data.get("precio_final")
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a cero.")
        return precio


class MetodoPagoForm(forms.ModelForm):
    class Meta:
        model = MetodoPago
        fields = ["nombre", "descripcion"]
        labels = {
            "nombre": "Método de pago",
            "descripcion": "Descripción",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["cliente", "paquete", "empleado", "precio_venta", "metodo_pago", "estado"]
        labels = {
            "cliente": "Cliente",
            "paquete": "Paquete",
            "empleado": "Empleado",
            "precio_venta": "Precio de venta",
            "metodo_pago": "Método de pago",
            "estado": "Estado",
        }
        widgets = {
            "cliente": Select(attrs={"class": "form-control"}),
            "paquete": Select(attrs={"class": "form-control"}),
            "empleado": Select(attrs={"class": "form-control"}),
            "precio_venta": NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.01"}),
            "metodo_pago": Select(attrs={"class": "form-control"}),
            "estado": Select(attrs={"class": "form-control"}),
        }

    def clean_precio_venta(self):
        precio = self.cleaned_data.get("precio_venta")
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a cero.")
        return precio


class InteraccionForm(forms.ModelForm):
    class Meta:
        model = Interaccion
        fields = ["cliente", "empleado", "tipo", "notas"]
        labels = {
            "cliente": "Cliente",
            "empleado": "Empleado",
            "tipo": "Tipo de interacción",
            "notas": "Notas",
        }
        widgets = {
            "cliente": Select(attrs={"class": "form-control"}),
            "empleado": Select(attrs={"class": "form-control"}),
            "tipo": Select(attrs={"class": "form-control"}),
            "notas": Textarea(attrs={"class": "form-control", "rows": 3}),
        }


# core/forms.py (continuación)
User = get_user_model()

class EmpleadoCreateForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        # Ajusta campos si tu Empleado usa otros nombres (ej. nombre/telefono)
        fields = ["email", "is_active", "is_staff", "groups"]
        labels = {"email": "Correo", "groups": "Roles"}

        widgets = {
            "groups": forms.CheckboxSelectMultiple,
        }

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.save_m2m()
        return user


class EmpleadoUpdateForm(forms.ModelForm):
    password1 = forms.CharField(label="Nueva contraseña", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirmar nueva contraseña", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ["email", "is_active", "is_staff", "groups"]
        labels = {"email": "Correo", "groups": "Roles"}
        widgets = {"groups": forms.CheckboxSelectMultiple}

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if (p1 or p2) and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        p1 = self.cleaned_data.get("password1")
        if p1:
            user.set_password(p1)
        if commit:
            user.save()
            self.save_m2m()
        return user
