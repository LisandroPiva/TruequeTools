from rest_framework import routers
from rest_framework.urls import path
from .api import *
from apptrueques import views

router = routers.DefaultRouter()

router.register('api/usuarios', UsuarioViewSet, basename='usuarios')
router.register('api/publicaciones', PublicacionViewSet, basename='publicaciones')
router.register('api/comentarios', ComentarioViewSet, basename='comentarios')
router.register('api/solicitudes', SolicitudViewSet, basename='solicitudes')
router.register('api/sucursales', SucursalViewSet, basename='sucursales')


urlpatterns = router.urls + [
     path('api/register', views.RegisterView, name='register')
]
