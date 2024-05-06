from rest_framework import serializers
from .models import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'fecha_de_nacimiento', 'sucursal_favorita', 'reputacion')
        read_only_fields = ('reputacion', )
        extra_kwargs = {'password': {'write_only': True}}


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = '__all__'
        read_only_fields = ('fecha', )

class ComentarioRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComentarioRespuesta
        fields = '__all__'
        read_only_fields = ('fecha', )

class ComentarioSerializer(serializers.ModelSerializer):
    respuestas = ComentarioRespuestaSerializer(many=True, read_only=True)
    class Meta:
        model = Comentario
        fields = '__all__'
        read_only_fields = ('fecha',  )

class PublicacionSerializer(serializers.ModelSerializer):   
    comentarios = ComentarioSerializer(many=True, read_only=True)
    class Meta:
        model = Publicacion
        fields = '__all__'
        read_only_fields=('fecha', 'estado', )