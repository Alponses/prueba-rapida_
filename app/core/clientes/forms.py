from django import forms
from .models import Cliente

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
