from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from apptrueques.models import Empleado

class EmpleadoBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            print("HOLAAAAAAAAAAAA")
            empleado = Empleado.objects.get(email=email)
            if empleado.check_password(password):
                return empleado
        except Empleado.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Empleado.objects.get(pk=user_id)
        except Empleado.DoesNotExist:
            return None
