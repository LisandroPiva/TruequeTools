from rest_framework import routers
from rest_framework.urls import path
from django.urls import include
from .api import *
from .views import *

router = routers.DefaultRouter()

router.register('usuarios', UsuarioViewSet, 'usuarios')
router.register('publicaciones', PublicacionViewSet, 'publicaciones')
router.register('comentarios', ComentarioViewSet, 'comentarios')
router.register('solicitudes', SolicitudViewSet, 'solicitudes')
router.register('sucursales', SucursalViewSet, 'sucursales')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
]