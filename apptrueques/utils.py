from django.db.models import Q
from .models import Publicacion, SolicitudDeIntercambio

def get_solicitudes_no_espera(user):
    # Obtener todas las publicaciones del usuario
    publicaciones = Publicacion.objects.filter(usuario_propietario=user)
    # Obtener todas las solicitudes relacionadas con estas publicaciones, tanto como publicacion_deseada como publicacion_a_intercambiar
    solicitudes = SolicitudDeIntercambio.objects.filter(
        Q(publicacion_deseada__in=publicaciones) | Q(publicacion_a_intercambiar__in=publicaciones)
    ).exclude(estado='ESPERA')
    return solicitudes.order_by('-fecha')