from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    reputacion = models.IntegerField(null=True, default=0)
    fecha_de_nacimiento = models.DateField()
    sucursal_favorita = models.ForeignKey(Sucursal, related_name="usuarios", on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'fecha_de_nacimiento']

    def __str__(self):
        return self.username

class Empleado(models.Model):
    sucursal_de_trabajo = models.ForeignKey(Sucursal, related_name="empleados", on_delete=models.CASCADE, null=True)
    dni = models.CharField(max_length=11, unique=True, default='', primary_key=True)
    nombre = models.CharField(max_length=150, null=False, unique=False, default='')
    is_staff = models.BooleanField(default=True)
    password = models.CharField(max_length=50, blank=False, null=False, default='')
    REQUIRED_FIELDS = ['password', 'dni', 'nombre', 'sucursal_de_trabajo']  

    def __str__(self):
        return 'empleado ' + self.nombre + ' dni ' + self.dni

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
    imagen = models.ImageField(upload_to="images", null=True, blank=True)
  
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        if not self.sucursal_destino:
            self.sucursal_destino = self.usuario_propietario.sucursal_favorita
        super().save(*args, **kwargs)


class SolicitudDeIntercambio(models.Model):
    publicacion_deseada = models.ForeignKey(Publicacion, related_name='solicitudes_recibidas', on_delete=models.CASCADE)
    publicacion_a_intercambiar = models.ForeignKey(Publicacion, related_name='solicitudes_enviadas', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    ESTADO_CHOICES = (
        ('ESPERA', 'Espera'),
        ('PENDIENTE', 'Pendiente'),
        ('EXITOSA', 'Exitosa'),
        ('FALLIDA', 'Fallida'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ESPERA')
    def __str__(self):
        return self.publicacion_a_intercambiar.usuario_propietario
    

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


