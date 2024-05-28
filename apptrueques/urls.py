from rest_framework import routers
from rest_framework.urls import path
from django.urls import include
from .api import *
from .views import *
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()

router.register('usuarios', UsuarioViewSet, 'usuarios')
router.register('publicaciones', PublicacionViewSet, 'publicaciones')
router.register('comentarios', ComentarioViewSet, 'comentarios')
router.register('solicitudes', SolicitudDeIntercambioViewSet, 'solicitudes')
router.register('sucursales', SucursalViewSet, 'sucursales')
router.register('categorias', CategoriaViewSet, 'categorias')
router.register('comentarios_respuesta', ComentarioRespuestaViewSet, 'comentarios_respuesta')
router.register('empleados', EmpleadoViewSet, 'empleados')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/adminview/sucursales/add', CreateSucursalView.as_view(), name="add-sucursal"),
    path('api/sucursal/<int:sucursal_id>/', SucursalInfo.as_view(), name="sucursal-info"),
    path('api/user-info/', UserInfoView.as_view(), name="user-info"),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/createPost/', CreatePostView.as_view(), name='createpost'),
    path('api/post/<int:publicacion_id>/', PostDetailView.as_view(), name='post_detail'),
    path('api/post/<int:publicacion_id>/comments/', CreateCommentView.as_view(), name='post_comment'),
    path('api/post/<int:publicacion_id>/comments/<int:comentario_id>/', CreateReplyView.as_view(), name='post_reply'),
    path('api/post/<int:publicacion_id>/comments_list/', PostComments.as_view(), name="post_comments"),
    path('api/adminview/employees/', EmployeesList.as_view(), name="employee_list"),
    path('api/login-worker/', LoginWorker.as_view(), name="login-worker"),
    path('api/search-posts/', SearchPostsView.as_view(), name='search-posts'),
    path('api/adminview/employees/add', CreateEmployeeView.as_view(), name="add-employee"),
    path('api/misProductos/', MisProductosView.as_view(), name="user_products"),
    path('api/create-solicitud/', CreateSolicitudView.as_view(), name="enviar_solicitud"),
    path('api/post/<int:publicacion_id>/solicitudes', MisSolicitudesView.as_view(), name="mis_solicitudes")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)       