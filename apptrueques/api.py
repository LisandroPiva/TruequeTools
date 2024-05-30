from .models import *
from rest_framework import viewsets, permissions
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q, Count

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    permission_classes = [permissions.IsAuthenticated]    
    serializer_class = UsuarioSerializer
    authentication_classes = [TokenAuthentication]


class PublicacionViewSet(viewsets.ModelViewSet):
    serializer_class = PublicacionSerializer
    permission_classes = [permissions.IsAuthenticated]    
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        # Obtener las IDs de las publicaciones deseadas con al menos una solicitud en estado diferente de "Espera"
        publicaciones_deseadas_no_espera = SolicitudDeIntercambio.objects.exclude(estado='ESPERA').values_list('publicacion_deseada', flat=True).distinct()

        # Obtener las IDs de las publicaciones a intercambiar con al menos una solicitud en estado diferente de "Espera"
        publicaciones_a_intercambiar_no_espera = SolicitudDeIntercambio.objects.exclude(estado='ESPERA').values_list('publicacion_a_intercambiar', flat=True).distinct()

        # Combinar ambas listas de IDs
        publicaciones_no_espera = set(publicaciones_deseadas_no_espera).union(set(publicaciones_a_intercambiar_no_espera))

        # Obtener todas las publicaciones excepto aquellas que están en la lista de IDs combinada
        queryset = Publicacion.objects.exclude(id__in=publicaciones_no_espera)

        return queryset.order_by('-fecha').distinct()


class SolicitudDeIntercambioViewSet(viewsets.ModelViewSet):
    queryset = SolicitudDeIntercambio.objects.all().order_by('-fecha')
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