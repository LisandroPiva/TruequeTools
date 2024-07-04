from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from rest_framework_simplejwt.tokens import RefreshToken

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    borrada = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre

class Notificacion(models.Model):
    contenido = models.CharField(max_length=200)
    leida = models.BooleanField(default=False)
    usuario = models.ForeignKey('Usuario', related_name='notificaciones', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.contenido

class Usuario(AbstractUser):
    reputacion = models.IntegerField(null=True, default=0)
    fecha_de_nacimiento = models.DateField()
    sucursal_favorita = models.ForeignKey(Sucursal, related_name="usuarios", on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="images", default="/images/userNoProfilePicture.jpg") 
    bloqueado = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'fecha_de_nacimiento']
    def __str__(self):
        return self.username

class Empleado(AbstractUser):
    sucursal_de_trabajo = models.ForeignKey(Sucursal, related_name="empleados", on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True, default='')
    username = models.CharField(max_length=150, unique=False)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'password', ]

    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='empleado_groups'  # Nombre de acceso inverso personalizado
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='empleado_permissions'  # Nombre de acceso inverso personalizado
    )

    def __str__(self):
        return 'empleado ' + self.username + ' email ' + self.email
    
    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre


class Publicacion(models.Model):
    usuario_propietario = models.ForeignKey(Usuario, related_name="publicaciones", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    sucursal_destino = models.ForeignKey(Sucursal, related_name="publicaciones", on_delete=models.CASCADE, blank=True, null=True)
    imagen = models.ImageField(upload_to="images", default="/images/noPostImage.jpg")
    fecha_fin_promocion = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        if not self.sucursal_destino:
            self.sucursal_destino = self.usuario_propietario.sucursal_favorita
        super().save(*args, **kwargs)

class SolicitudDeIntercambio(models.Model):
    publicacion_deseada = models.ForeignKey(Publicacion, related_name='solicitudes_recibidas', on_delete=models.CASCADE)
    publicacion_a_intercambiar = models.ForeignKey(Publicacion, related_name='solicitudes_enviadas', on_delete=models.CASCADE)
    fecha_del_intercambio = models.DateTimeField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    ESTADO_CHOICES = (
        ('ESPERA', 'Espera'),
        ('PENDIENTE', 'Pendiente'),
        ('EXITOSA', 'Exitosa'),
        ('FALLIDA', 'Fallida'),
        ('RECHAZADA', 'Rechazada'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ESPERA')
    def __str__(self):
        return self.publicacion_a_intercambiar.usuario_propietario.username
    
        
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio_unitario = models.FloatField()

    def __str__(self):
        return self.nombre

class VentaProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)

class Venta(models.Model):
    intercambio = models.OneToOneField(SolicitudDeIntercambio, related_name='venta', on_delete=models.CASCADE, blank=True, null=True)
    productos_vendidos = models.ManyToManyField(VentaProducto, related_name='ventas')

    def precio_total(self):
        total = 0
        for venta_producto in self.productos_vendidos.all():
            producto = venta_producto.producto
            cantidad = venta_producto.cantidad
            total += producto.precio_unitario * cantidad
        return total


class ComentarioRespuesta(models.Model):
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario_propietario = models.ForeignKey(Usuario, related_name="respuestas_publicadas", on_delete=models.CASCADE)
    def __str__(self):
        return f"Respuesta de {self.usuario_propietario.username}"

class Comentario(models.Model):
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    publicacion = models.ForeignKey(Publicacion, related_name="comentarios", on_delete=models.CASCADE)
    usuario_propietario = models.ForeignKey(Usuario, related_name="comentarios", on_delete=models.CASCADE)
    respuesta = models.OneToOneField(ComentarioRespuesta, related_name='comentario', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Comentario de {self.usuario_propietario.username}"
    
    def getReply(self):
        return self.respuesta


