from rest_framework import serializers
from .models import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['email', 'username', 'password', 'reputacion', 'fecha_de_nacimiento', 'sucursal_favorita']
        read_only_fields = ('reputacion', )
        extra_kwargs = {'password': {'write_only': True}}

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ('id', 'nombre', 'direccion')

class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = ('id', 'usuario_propietario', 'titulo', 'fecha', 'descripcion', 'imagen')
        read_only_fields=('fecha',  )

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ('id', 'publicacion_deseada','publicacion_a_intercambiar','fecha' )
        read_only_fields = ('fecha', )

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ('id', 'contenido', 'fecha', 'publicacion', 'usuario_propietario', 'respuesta')
        read_only_fields = ('fecha', )

