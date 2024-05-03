from rest_framework import routers
from .api import *
from apptrueques import views

router = routers.DefaultRouter()

router.register('api/usuarios', UsuarioViewSet, 'usuarios')
router.register('api/publicaciones', PublicacionViewSet, 'publicaciones')
router.register('api/comentarios', ComentarioViewSet, 'comentarios')
router.register('api/solicitudes', SolicitudViewSet, 'solicitudes')
router.register('api/sucursales', SucursalViewSet, 'sucursales')
router.register('api/login', views.login, '/login')
router.register('api/register', views.register, '/register')
router.register('api/profile', views.profile, '/profile')

urlpatterns = router.urls