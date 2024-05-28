from .models import *
from rest_framework import viewsets, permissions
from .serializers import *
from rest_framework.authentication import TokenAuthentication

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    permission_classes = [permissions.IsAuthenticated]    
    serializer_class = UsuarioSerializer
    authentication_classes = [TokenAuthentication]

class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = Publicacion.objects.all().order_by('-fecha')
    serializer_class = PublicacionSerializer
    permission_classes = [permissions.IsAuthenticated]    
    authentication_classes = [TokenAuthentication]

class SolicitudDeIntercambioViewSet(viewsets.ModelViewSet):
    queryset = SolicitudDeIntercambio.objects.all()
    permission_classes = [permissions.IsAuthenticated]    
    serializer_class = SolicitudDeIntercambioSerializer
    authentication_classes = [TokenAuthentication]

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    permission_classes = [permissions.IsAuthenticated]    
    serializer_class = ComentarioSerializer
    authentication_classes = [TokenAuthentication]

class ComentarioRespuestaViewSet(viewsets.ModelViewSet):
    queryset = ComentarioRespuesta.objects.all()
    permission_classes = [permissions.IsAuthenticated]    
    serializer_class = ComentarioRespuestaSerializer
    authentication_classes = [TokenAuthentication]

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    permission_classes = [permissions.AllowAny]     
    serializer_class = SucursalSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    permission_classes = [permissions.AllowAny]    
    serializer_class = CategoriaSerializer
        
class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    permission_classes = [permissions.AllowAny]    
    serializer_class = EmpleadoSerializer