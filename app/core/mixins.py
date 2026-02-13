# core/mixins.py
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class PermissionRedirectMixin(AccessMixin):
    """
    - Si no está logueado -> redirect a 'login'
    - Si está logueado pero NO tiene permiso -> redirect a 'access_denied'
    """
    required_perm = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if self.required_perm and not request.user.has_perm(self.required_perm):
            return redirect("access_denied")
        return super().dispatch(request, *args, **kwargs)
