from .models import *
from rest_framework import viewsets, permissions
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q, Count

from .models import Empleado

class SolicitudDeIntercambioViewSet(viewsets.ModelViewSet):
    serializer_class = SolicitudDeIntercambioSerializer
    queryset = SolicitudDeIntercambio.objects.all().order_by('fecha_del_intercambio')
    permission_classes = [permissions.IsAuthenticated]    
    authentication_classes = [TokenAuthentication]
    # def get_queryset(self, request):
    #     # Obtener el parámetro de la URL que contiene la sucursal
    #     sucursal_param = request.query_params.get('sucursalTrabajo', None)

    #     # Verificar si se proporciona la sucursal en los parámetros de la URL
    #     if sucursal_param is not None:
    #         # Filtrar las solicitudes de intercambio por la sucursal proporcionada y estado PENDIENTE
    #         queryset = SolicitudDeIntercambio.objects.filter(
    #             publicacion_deseada__sucursal_destino=sucursal_param,
    #             estado='PENDIENTE'
    #         ).order_by('fecha_del_intercambio')
    #     else:
    #         # Si no se proporciona la sucursal en los parámetros de la URL, devolver todas las solicitudes de intercambio
    #         queryset = SolicitudDeIntercambio.objects.all().order_by('fecha_del_intercambio')

    #     return queryset

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    permission_classes = [permissions.IsAuthenticated]    
    serializer_class = UsuarioSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return super().get_queryset()


class PublicacionViewSet(viewsets.ModelViewSet):
    serializer_class = PublicacionSerializer
    permission_classes = [permissions.AllowAny]    
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

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = VentaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductoSerializer