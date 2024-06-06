from rest_framework import permissions
from .models import Empleado

class IsEmpleadoOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Verificar si el usuario ha sido autenticado mediante un token
        if request.auth:
            try:
                # Verificar si el token pertenece a un empleado
                empleado = Empleado.objects.get(token=request.auth)
                return True
            except Empleado.DoesNotExist:
                return False
        return False
