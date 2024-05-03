from .models import *
from rest_framework import viewsets, permissions
from .serializers import *
from .views import RegisterView


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    permission_classes = [permissions.AllowAny]    # <---- El "AllowAny" luego hay que cambiarlo, una vez hecho el sistema de inicio de sesión
    serializer_class = UsuarioSerializer

class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = Publicacion.objects.all()
    permission_classes = [permissions.AllowAny]    
    serializer_class = PublicacionSerializer

class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    permission_classes = [permissions.AllowAny]    
    serializer_class = SolicitudSerializer

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    permission_classes = [permissions.AllowAny]    
    serializer_class = ComentarioSerializer

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    permission_classes = [permissions.AllowAny]     
    serializer_class = SucursalSerializer

        
     
