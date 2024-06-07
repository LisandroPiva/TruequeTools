from rest_framework import serializers
from .models import *

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    sucursal_de_trabajo = SucursalSerializer()
    class Meta:
        model = Empleado
        fields = ('id','email', 'sucursal_de_trabajo',  'password', 'is_staff', )
        read_only_fields = ('is_staff', )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['is_staff'] = True
        empleado = Empleado(**validated_data)
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