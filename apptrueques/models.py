from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre





class UsuarioManager(BaseUserManager):
    # Administrador personalizado para el modelo Usuario

    def create_user(self, email, password=None, **extra_fields):
        # Método para crear un usuario regular
        if not email:
            raise ValueError('El email es obligatorio.') # Se asegura de que se proporcione un email
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields) # Crea un nuevo usuario con el email normalizado y otros campos extra
        user.set_password(password) # Establece la contraseña del usuario
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Método para crear un superusuario
        extra_fields.setdefault('is_staff', True) # Establece is_staff en True
        extra_fields.setdefault('is_superuser', True) # Establece is_superuser en True

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.') # Se asegura de que is_staff sea True para superusuarios
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.') # Se asegura de que is_superuser sea True para superusuarios

        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser):
    # Definición del modelo Usuario

    # Campos del modelo
    email = models.EmailField(unique=True) # Correo electrónico del usuario
    nombre = models.CharField(max_length=100) # Nombre del usuario
    reputacion = models.IntegerField(null=True) # Reputación del usuario
    fecha_de_nacimiento = models.DateField(auto_now_add=True) # Fecha de nacimiento del usuario
    sucursal_favorita = models.ForeignKey(Sucursal, related_name="usuarios", null=True, on_delete=models.SET_NULL) # Sucursal favorita del usuario
    is_active = models.BooleanField(default=True) # Indica si el usuario está activo
    is_staff = models.BooleanField(default=False) # Indica si el usuario es miembro del personal administrativo

    objects = UsuarioManager() # Administrador del modelo Usuario

    USERNAME_FIELD = 'email' # Campo utilizado para identificar al usuario durante el inicio de sesión
    REQUIRED_FIELDS = ['nombre'] # Campos requeridos para crear un usuario

    def __str__(self):
        # Método que retorna una representación en cadena del objeto Usuario
        return self.email

class Publicacion(models.Model):
    usuario_propietario = models.ForeignKey(Usuario, related_name="publicaciones", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.TextField()
    imagen = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.titulo
    # sucursal destino?

class Comentario(models.Model):
    contenido = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    publicacion = models.ForeignKey(Publicacion, related_name="comentarios", on_delete=models.CASCADE)
    usuario_propietario = models.ForeignKey(Usuario, related_name="comentarios", on_delete=models.CASCADE)
    respuesta = models.ForeignKey('self', related_name='respuestas', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.usuario_propietario.nombre

class Solicitud(models.Model):
    publicacion_deseada = models.ForeignKey(Publicacion, related_name='solicitudes_recibidas', on_delete=models.CASCADE)
    publicacion_a_intercambiar = models.ForeignKey(Publicacion, related_name='solicitudes_enviadas', on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.publicacion_a_intercambiar.usuario_propietario

    
