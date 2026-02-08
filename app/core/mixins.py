from django.shortcuts import redirect
from django.urls import reverse

class PermissionRedirectMixin:
    """
    - Si no está autenticado -> login
    - Si es superuser -> pasa
    - Si tiene required_perm -> pasa
    - Si no -> redirect a /403/
    """
    required_perm = None
    denied_url_name = "access_denied"  # ruta global del proyecto

    def has_permission(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if getattr(user, "is_superuser", False):
            return True
        if not self.required_perm:
            return True
        return user.has_perm(self.required_perm)

    def handle_no_permission(self):
        # aquí puedes mandar a 404 si quieres ocultar módulos
        return redirect(self.denied_url_name)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
