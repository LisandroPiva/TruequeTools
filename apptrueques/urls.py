from rest_framework import routers
from rest_framework.urls import path
from django.urls import include
from .api import *
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()

router.register('usuarios', UsuarioViewSet, 'usuarios')
router.register('publicaciones', PublicacionViewSet, 'publicaciones')
router.register('comentarios', ComentarioViewSet, 'comentarios')
router.register('solicitudes', SolicitudDeIntercambioViewSet, 'solicitudes')
router.register('sucursales', SucursalViewSet, 'sucursales')
router.register('categorias', CategoriaViewSet, 'categorias')
router.register('comentarios_respuesta', ComentarioRespuestaViewSet, 'comentarios_respuesta')
router.register('empleados', EmpleadoViewSet, 'empleados')
router.register('ventas', VentaViewSet, 'ventas')
router.register('productos', ProductoViewSet, 'productos')
router.register('notificaciones', NotificacionViewSet, 'notificaciones')



urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/adminview/sucursales/add', CreateSucursalView.as_view(), name="add-sucursal"),
    path('api/adminview/sucursales/', CreateSucursalView.as_view(), name="search-sucursal"),
    path('api/adminview/sucursales/<int:sucursal_id>/', CreateSucursalView.as_view(), name="delete-sucursal"),
    path('api/adminview/post/<int:publicacion_id>/', PostDetailAdminView.as_view(), name="delete-post"),


    path('api/sucursal/<int:sucursal_id>/', SucursalInfo.as_view(), name="sucursal-info"),
    path('api/user-info/', UserInfoView.as_view(), name="user-info"),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/createPost/', CreatePostView.as_view(), name='createpost'),
    path('api/post/<int:publicacion_id>/', PostDetailView.as_view(), name='post_detail'),
    path('api/post-admin/<int:publicacion_id>/', PostDetailAdminView.as_view(), name='post_detail_admin'),
    path('api/post-admin/<int:publicacion_id>/comments/', CommentAdminView.as_view(), name='post_comment_admin'),
    path('api/post-admin/<int:publicacion_id>/comments/<int:comentario_id>/delete/', CommentAdminView.as_view(), name='delete_comment'),

    path('api/admin/publicaciones/', PostListAdmin.as_view(), name="postlist_admin"),
    path('api/post/<int:publicacion_id>/comments/', CommentView.as_view(), name='post_comment'),
    path('api/post/<int:publicacion_id>/comments/<int:comentario_id>/delete/', CommentView.as_view(), name='delete_comment'),
    path('api/post/<int:publicacion_id>/comments/<int:comentario_id>/', ReplyView.as_view(), name='post_reply'),

    path('api/post/<int:publicacion_id>/comments_list/', PostComments.as_view(), name="post_comments"),
    path('api/adminview/employees/', EmployeesList.as_view(), name="employee_list"),
    path('api/login-worker/', LoginWorker.as_view(), name="login-worker"),
    path('api/search-posts/', SearchPostsView.as_view(), name='search-posts'),
    path('api/adminview/search-users/',  UserView.as_view(), name="search_users"),
    path('api/adminview/toggle-block/<int:usuario_id>/',  UserView.as_view(), name="toggle_block_users"),
    path('api/adminview/employees/add', EmployeeView.as_view(), name="add-employee"),
    path('api/employee/<int:employee_id>/', EmployeeView.as_view(), name="delete-employee"),

    path('api/employee/<int:employee_id>/detail/', EmployeeDetailView.as_view(), name="employee_detail"),  # Updated path for detail view
    path('api/misProductos/', MisProductosView.as_view(), name="user_products"),
    path('api/create-solicitud/', SolicitudView.as_view(), name="enviar_solicitud"),
    path('api/mis-solicitudes/<int:solicitud_id>/', SolicitudView.as_view(), name="aceptar_solicitud"),
    path('api/mis-solicitudes/<int:solicitud_id>/', SolicitudView.as_view(), name='delete_solicitud'),
    path('api/mis-solicitudes/', SolicitudView.as_view(), name='ver_solicitudes'),

    path('api/employee/solicitudes/success/', TruequesExitososView.as_view(), name="trueques_exitosos"),
    path('api/employee/solicitudes/failure/', TruequesFallidosView.as_view(), name="trueques_fallidos"),

    path('api/employee/solicitudes/', SolicitudesEmployeeView.as_view(), name='employee_solicitudes'),
    path('api/employee/solicitudes/today/', SolicitudesHoyEmployeeView.as_view(), name='employee_solicitudes_today'),
    path('api/employee/solicitudes/<int:solicitud_id>/', SolicitudesEmployeeView.as_view(), name='solicitud_detail'),

    path('api/employee/solicitudes/<int:solicitud_id>/ventas/', VentasView.as_view(), name="registrar_venta"),
    path('api/employee/solicitudes/<int:solicitud_id>/ventas/', VentasView.as_view(), name="ver_venta"), 


    path('api/post/<int:publicacion_id>/solicitudes/', MisSolicitudesView.as_view(), name="mis_solicitudes"),
    path('api/solicitudes/<int:solicitud_id>/cancel/', CancelarSolicitudView.as_view(), name="cencelar_solicitud"),
    path('api/historial/', HistorialDeSolicitudesView.as_view(), name="historial"),
    path('api/mis-notificaciones/', NotificacionView.as_view(), name="ver_notificaciones"),
    path('api/mis-notificaciones/<int:notificacion_id>/', NotificacionView.as_view(), name="marcar_leida"),
    path('api/adminview/stats/', EstadisticasView.as_view(), name="estadisticas"),
    path('api/mis-publicaciones/<int:publicacion_id>/', PostDetailView.as_view(), name="borrar_post"),
    path('api/mis-publicaciones/<int:publicacion_id>/destacar/', DestacarProductoView.as_view(), name="destacar_producto"),

    



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)       