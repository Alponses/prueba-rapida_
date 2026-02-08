from django.shortcuts import render


# core/clientes/views.py
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Cliente
from .forms import ClienteForm

class ClienteListView(ListView):
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

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_url = reverse_lazy("clientes:cliente_list")

    def form_valid(self, form):
        messages.success(self.request, "Cliente creado correctamente.")
        return super().form_valid(form)

class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_url = reverse_lazy("clientes:cliente_list")

    def form_valid(self, form):
        messages.success(self.request, "Cliente actualizado.")
        return super().form_valid(form)

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = "clientes/cliente_confirm_delete.html"
    success_url = reverse_lazy("clientes:cliente_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        nombre = getattr(obj, "nombre", str(obj))  
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Cliente {nombre} eliminado correctamente.")
        return response
