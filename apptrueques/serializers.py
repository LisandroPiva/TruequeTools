from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'
class EmpleadoSerializer(serializers.ModelSerializer):
    sucursal_de_trabajo = serializers.PrimaryKeyRelatedField(queryset=Sucursal.objects.all(), write_only=True, required=False, allow_null=True)
    sucursal = SucursalSerializer(read_only=True, source='sucursal_de_trabajo')

    class Meta:
        model = Empleado
        fields = ('id', 'email', 'sucursal_de_trabajo', 'sucursal', 'password', 'is_staff')
        read_only_fields = ('is_staff', )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['is_staff'] = True
        sucursal = validated_data.pop('sucursal_de_trabajo', None)  # Utiliza None como valor por defecto
        empleado = Empleado.objects.create(**validated_data)
        
        if sucursal:
            empleado.sucursal_de_trabajo = sucursal
        
        empleado.set_password(validated_data['password'])
        empleado.save()
        return empleado


    
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class VentaProductoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer() 
    class Meta:
        model = VentaProducto
        fields = ['producto', 'cantidad']


class VentaSerializer(serializers.ModelSerializer):
    productos_vendidos = VentaProductoSerializer(many=True)

    class Meta:
        model = Venta
        fields = '__all__'

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = "__all__"

class UsuarioSerializer(serializers.ModelSerializer):
    sucursal_favorita = serializers.PrimaryKeyRelatedField(queryset=Sucursal.objects.all(), required=False)
    notificaciones = NotificacionSerializer(many=True, read_only=True)
    new_password = serializers.CharField(write_only=True, required=False)  # Campo para manejar la nueva contraseña
  
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'fecha_de_nacimiento', 'sucursal_favorita', 'reputacion', 'is_staff', 'bloqueado', 'avatar', 'notificaciones', 'new_password')
        read_only_fields = ('reputacion', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False},  # Permitir actualizar username de forma opcional
            'email': {'required': False},     # Permitir actualizar email de forma opcional
            'avatar': {'required': False}     # Permitir actualizar avatar de forma opcional
        }

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password', None)
        if new_password:
            instance.set_password(new_password)

        # Actualizar sucursal_favorita si se proporciona en validated_data
        sucursal_favorita = validated_data.get('sucursal_favorita', None)
        if sucursal_favorita is not None:
            instance.sucursal_favorita = sucursal_favorita

        # Actualizar username si se proporciona en validated_data
        username = validated_data.get('username', None)
        if username:
            instance.username = username

        # Actualizar email si se proporciona en validated_data
        email = validated_data.get('email', None)
        if email:
            instance.email = email

        # Actualizar avatar si se proporciona en validated_data
        avatar = validated_data.get('avatar', None)
        if avatar is not None:
            instance.avatar = avatar

        return super().update(instance, validated_data)


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'



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
    class Meta:
        model = Publicacion
        fields = '__all__'
        read_only_fields=('fecha', )
    
    def get_comentarios(self, publicacion):
        return self.to_representation(publicacion)['comentarios']
    
    def get_solicitudes_recibidas(self, publicacion):
        queryset = SolicitudDeIntercambio.objects.filter(
            publicacion=publicacion,
            estado='PENDIENTE'
        ).order_by('fecha_del_intercambio')
        return SolicitudDeIntercambioSerializer(queryset, many=True).data
    


class SolicitudDeIntercambioSerializer(serializers.ModelSerializer):
    venta = VentaSerializer(read_only=True)
    publicacion_a_intercambiar = PublicacionSerializer(read_only=True)
    publicacion_deseada = PublicacionSerializer(read_only=True)
    class Meta:
        model = SolicitudDeIntercambio
        fields = '__all__'
        read_only_fields = ('fecha','fecha_del_intercambio', )

    def get_venta(self, publicacion):
         return self.to_representation(publicacion)['productos_vendidos']