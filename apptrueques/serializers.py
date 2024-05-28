from rest_framework import serializers
from .models import *

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'
        read_only_fields = ('is_staff', )
        extra_kwargs = {'password': {'write_only': True}}

class UsuarioSerializer(serializers.ModelSerializer):
    sucursal_favorita = SucursalSerializer(read_only=True)    
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'fecha_de_nacimiento', 'sucursal_favorita', 'reputacion', 'is_staff')
        read_only_fields = ('reputacion', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class SolicitudDeIntercambioSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudDeIntercambio
        fields = '__all__'
        read_only_fields = ('fecha', 'estado', )

class ComentarioRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComentarioRespuesta
        fields = '__all__'
        read_only_fields = ('fecha', )

class ComentarioSerializer(serializers.ModelSerializer):
    respuesta = ComentarioRespuestaSerializer(read_only=True)
    usuario_propietario = UsuarioSerializer(read_only=True)
    class Meta:
        model = Comentario
        fields = ('id', 'fecha', 'contenido', 'respuesta', 'publicacion_id', 'usuario_propietario')
        read_only_fields = ('fecha', )

class PublicacionSerializer(serializers.ModelSerializer):   
    comentarios = ComentarioSerializer(many=True, read_only=True)
    sucursal_destino = SucursalSerializer(read_only=True)
    usuario_propietario = UsuarioSerializer(read_only=True)
    solicitudes_recibidas = SolicitudDeIntercambioSerializer(many=True, read_only=True)
    class Meta:
        model = Publicacion
        fields = '__all__'
        read_only_fields=('fecha',  )
    
    def get_comentarios(self, publicacion):
        return self.to_representation(publicacion)['comentarios']
    
    def get_solicitudes(self, publicacion):
        return self.to_representation(publicacion)['solicitudes_recibidas']
