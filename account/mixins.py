from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

from .models import User

class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is manager """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class ManagerRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is manager """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.type==User.Types.MANAGER:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class CustomerRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is manager """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.type==User.Types.CUSTOMER:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)