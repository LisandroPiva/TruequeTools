from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_406_NOT_ACCEPTABLE, HTTP_409_CONFLICT,HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.authtoken.models import Token
from .models import Usuario, Empleado
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from .api import PublicacionViewSet
from .utils import *
from datetime import datetime, timedelta


@permission_classes([AllowAny])
class RegisterView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        print(request.data)
        if len(request.data.get('password', '')) < 6:
            return Response({"error": "La contraseña debe tener al menos 6 caracteres"}, status=HTTP_400_BAD_REQUEST)
        if Usuario.objects.filter(email=request.data['email']).exists():
            return Response({"error": "El correo electrónico ya está en uso"}, status=HTTP_409_CONFLICT)
        if serializer.is_valid():
            try:
                
                sucursal = get_object_or_404(Sucursal, pk=request.data['sucursal_favorita'])
                fecha_nacimiento = datetime.strptime(request.data['fecha_de_nacimiento'], '%Y-%m-%d').date()
                fecha_actual = datetime.now().date()
                edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
                if (edad < 18):
                    return Response({"error": "Para registrarse en el sistema debe ser mayor de edad"}, status=HTTP_406_NOT_ACCEPTABLE)
                    
                usuario = Usuario.objects.create_user(
                    username=request.data['username'],
                    email=request.data['email'],
                    password=request.data['password'],
                    fecha_de_nacimiento=request.data['fecha_de_nacimiento'],  
                    sucursal_favorita=sucursal
                )
                token, created = Token.objects.get_or_create(user=usuario)
                print(serializer.validated_data)
                response_data = {
                    'token': token.key,
                    'user': serializer.data,
                    'sucursal favorita': sucursal.nombre
                }
                return Response(response_data, status=HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, email=email, password=password)      
        if user is None:
            return Response({"error": "invalid credentials"}, status=HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UsuarioSerializer(instance=user)
        return Response({'token': token.key, 'user': serializer.data}, status=HTTP_200_OK)



@permission_classes([AllowAny])
class LoginWorker(APIView):
    def post(self, request):
        print(request.data)
        dni = request.data['dni']
        password = request.data['password']
        try:
            empleado = Empleado.objects.get(pk=dni)           
            print(empleado.password)
            if (empleado is not None and empleado.password == password):
                    
                    serializer = EmpleadoSerializer(instance=empleado)
                    return Response(serializer.data, status=HTTP_200_OK)
            else:
                return Response({"detail": "Credenciales inválidas"}, status=HTTP_404_NOT_FOUND)
        except Empleado.DoesNotExist:
            return Response({"detail": "Credenciales inválidas"}, status=HTTP_404_NOT_FOUND)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ProfileView(APIView):
    def get(self, request):
        serializer = UsuarioSerializer(instance=request.user)
        return Response({"Usuario logueado": serializer.data}, status=HTTP_200_OK)
    


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CreatePostView(APIView):
    def post(self, request):
        serializer = PublicacionSerializer(data=request.data)
        print("DATA", request.data)
        if serializer.is_valid():
            suc_destino = Sucursal.objects.get(pk=request.data['sucursal_destino'])
            publicacion = serializer.save(usuario_propietario=request.user, sucursal_destino = suc_destino)  
            response_data = PublicacionSerializer(publicacion).data 
            print("RESPONSE", response_data) 
            return Response(response_data, status=HTTP_201_CREATED) 
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
class CreateSucursalView(APIView):
    def post(self, request):
        serializer = SucursalSerializer(data=request.data)
        if (serializer.is_valid()):
            sucursal = serializer.save()
            response_data = SucursalSerializer(sucursal).data
            return Response(response_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        


class CreateEmployeeView(APIView):
    def post(self, request):
        serializer = EmpleadoSerializer(data=request.data)
        if (serializer.is_valid()):
            empleado = serializer.save()
            response_data = EmpleadoSerializer(empleado).data
            print(response_data)
            return Response(response_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CommentView(APIView):
    def post(self, request, publicacion_id):
        try:
            publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
        except Publicacion.DoesNotExist:
            return Response({"detail": "La publicación que deseas comentar ya no está disponible"}, status=HTTP_404_NOT_FOUND)
        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(publicacion=publicacion, usuario_propietario=request.user)  
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
    def delete(self, request, publicacion_id, comentario_id):
        try:
            publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
            comentario = get_object_or_404(Comentario, pk=comentario_id, publicacion=publicacion, usuario_propietario=request.user)
        except (Publicacion.DoesNotExist, Comentario.DoesNotExist):
            return Response({"detail": "El comentario o la publicación no está disponible"}, status=HTTP_404_NOT_FOUND)
        
        comentario.delete()
        return Response(status=HTTP_204_NO_CONTENT)
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ReplyView(APIView):
    def post(self, request, publicacion_id, comentario_id):
        try:
            comentario_original = get_object_or_404(Comentario, pk=comentario_id)
        except Comentario.DoesNotExist:
            return Response({"detail": "el comentario que deseas responder ya no está disponible"}, status=HTTP_404_NOT_FOUND)
        try:
            publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
        except Publicacion.DoesNotExist:
            return Response({"detail": "la publicacion ya no está disponible"}, status=HTTP_404_NOT_FOUND)
        
        if publicacion.usuario_propietario.id != request.user.id:
            return Response({"detail": "Solo el propietario de la publicación puede responder a los comentarios"}, status=HTTP_403_FORBIDDEN)
        
        request.data['usuario_propietario'] = request.user.id
        
        serializer = ComentarioRespuestaSerializer(data=request.data)
        if serializer.is_valid():
            respuesta = serializer.save()
            comentario_original.respuesta = respuesta
            comentario_original.save()
            serializer.save()  
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    # def delete(self, request, publicacion_id, respuesta_id):
    #     print(publicacion_id) 
    #     print(respuesta_id)
    #     try:
            
    #         publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
    #         respuesta = get_object_or_404(ComentarioRespuesta, pk=respuesta_id, publicacion=publicacion, usuario_propietario=request.user)
    #     except (Publicacion.DoesNotExist, ComentarioRespuesta.DoesNotExist):
    #         return Response({"detail": "El comentario o la publicación no está disponible"}, status=HTTP_404_NOT_FOUND)
        
    #     respuesta.delete()
    #     return Response(status=HTTP_204_NO_CONTENT)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PostDetailView(APIView):
    def get(self, request, publicacion_id):
        try:
            publicacion = Publicacion.objects.get(pk=publicacion_id)
            serializer = PublicacionSerializer(publicacion)
            print(serializer.data)
            return Response(serializer.data, status=HTTP_200_OK)
        except Publicacion.DoesNotExist:
            return Response({"detail": "La publicación que deseas ver no está disponible"}, status=HTTP_404_NOT_FOUND)
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class EmployeeDetailView(APIView):
    def get(self, request, employee_id):
        try:
            employee = Publicacion.objects.get(pk=employee_id)
            serializer = PublicacionSerializer(employee)
            print(serializer.data)
            return Response(serializer.data, status=HTTP_200_OK)
        except Publicacion.DoesNotExist:
            return Response({"detail": "El empleado que deseas ver no está disponible"}, status=HTTP_404_NOT_FOUND)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserInfoView(APIView):
     def get(self, request):
        user = request.user
        serializer = UsuarioSerializer(user)
        return Response(serializer.data)
     

class SucursalInfo(APIView):
    def get(self, request, sucursal_id):
        try:
            sucursal = Sucursal.objects.get(pk=sucursal_id)
            serializer = SucursalSerializer(sucursal)
            return Response(serializer.data, status=HTTP_200_OK)
        except Publicacion.DoesNotExist:
            return Response({"detail": "No existe sucursal con ese id"}, status=HTTP_404_NOT_FOUND)



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PostComments(APIView):
    def get(self, request, publicacion_id):
        try:
            publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
        except Publicacion.DoesNotExist:
            return Response({"detail": "La publicación no está disponible"}, status=HTTP_404_NOT_FOUND)
        serializer = PublicacionSerializer(publicacion)
        comentarios = serializer.get_comentarios(publicacion)
        return Response(comentarios)
    
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class EmployeesList(APIView):
    def get(self, request):
        empleados = Empleado.objects.all()
        serializer = EmpleadoSerializer(empleados, many=True)
        return Response(serializer.data)
    

class SearchPostsView(APIView):
    def get(self, request):
        # Obtén el queryset de PublicacionViewSet
        viewset = PublicacionViewSet()
        viewset.request = request  # Necesario si el método get_queryset depende del request
        queryset = viewset.get_queryset()
        
        # Filtra por título si hay un query param 'q'
        query = request.query_params.get('q', None)
        if query:
            queryset = queryset.filter(titulo__icontains=query)
            
        # Serializa y retorna la respuesta
        serializer = PublicacionSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MisProductosView(APIView):
    def get(self, request):
        user = request.user

        # Obtener IDs de las publicaciones deseadas con al menos una solicitud en estado diferente de "Espera"
        publicaciones_deseadas_no_espera = SolicitudDeIntercambio.objects.exclude(estado='ESPERA').values_list('publicacion_deseada', flat=True).distinct()

        # Obtener IDs de las publicaciones a intercambiar con al menos una solicitud en estado diferente de "Espera"
        publicaciones_a_intercambiar_no_espera = SolicitudDeIntercambio.objects.exclude(estado='ESPERA').values_list('publicacion_a_intercambiar', flat=True).distinct()

        # Combinar ambas listas de IDs
        publicaciones_no_espera = set(publicaciones_deseadas_no_espera).union(set(publicaciones_a_intercambiar_no_espera))

        # Filtrar las publicaciones del usuario excluyendo aquellas en la lista de IDs combinada
        queryset = Publicacion.objects.filter(usuario_propietario=user).exclude(id__in=publicaciones_no_espera)

        serializer = PublicacionSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SolicitudView(APIView):
    def post(self, request): ##este método se ejecuta cuando intercambia un prod
        publicacion_deseada_id = request.data.get('publicacion_deseada')
        publicacion_a_intercambiar_id = request.data.get('publicacion_a_intercambiar')
        try:
            publicacion_deseada = Publicacion.objects.get(id=publicacion_deseada_id)
            publicacion_a_intercambiar = Publicacion.objects.get(id=publicacion_a_intercambiar_id)
            print(publicacion_deseada.categoria, publicacion_a_intercambiar.categoria)
            if publicacion_deseada.categoria != publicacion_a_intercambiar.categoria:
                return Response({'error': 'Las publicaciones deben ser de la misma categoría.'}, status=HTTP_400_BAD_REQUEST)
            
            fecha = request.data.get('fecha_del_intercambio')
            print(fecha)
            if fecha:
                fecha = parse_datetime(fecha)
                print(fecha)
                if not fecha:
                    return Response({'error': 'Formato de fecha inválido.'}, status=HTTP_404_NOT_FOUND)
                if fecha < datetime.today():
                    return Response({'error': 'Formato de fecha inválido.'}, status=HTTP_404_NOT_FOUND)

            
            solicitud = SolicitudDeIntercambio.objects.create(
                publicacion_deseada=publicacion_deseada,
                publicacion_a_intercambiar=publicacion_a_intercambiar,
                estado='ESPERA',
                fecha_del_intercambio = fecha,
            )
            serializer = SolicitudDeIntercambioSerializer(solicitud)
            print(serializer.data)
            return Response(serializer.data, status=HTTP_201_CREATED)
    
        except Publicacion.DoesNotExist:
            return Response({'error': 'Publicación no encontrada.'}, status=HTTP_404_NOT_FOUND)
         
    def delete(self, request, solicitud_id): ##este método se ejecuta cuando rechaza una solicitud
        try:
            solicitud = SolicitudDeIntercambio.objects.get(id=solicitud_id, usuario=request.user)
            solicitud.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except SolicitudDeIntercambio.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada.'}, status=HTTP_404_NOT_FOUND)

    def patch(self, request, solicitud_id):
        print("Entrando al método patch")

        try:
            solicitud = SolicitudDeIntercambio.objects.get(id=solicitud_id)
            print(f"Solicitud encontrada: {solicitud.id}")
        except SolicitudDeIntercambio.DoesNotExist:
            print("Solicitud no encontrada")
            return Response(status=HTTP_404_NOT_FOUND)

        data = {'estado': 'PENDIENTE'}
        serializer = SolicitudDeIntercambioSerializer(solicitud, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print(f"Estado actualizado a: {solicitud.estado}")

            # Eliminar otras solicitudes para la misma publicación deseada
            otras_solicitudes = SolicitudDeIntercambio.objects.filter(
                publicacion_deseada=solicitud.publicacion_deseada,
                estado='ESPERA'
            ).exclude(id=solicitud_id)

            otras_solicitudes_count = otras_solicitudes.count()
            print(f"Número de otras solicitudes a eliminar: {otras_solicitudes_count}")

            otras_solicitudes.delete()
            print("Otras solicitudes eliminadas")

            return Response(status=HTTP_204_NO_CONTENT)

        print(f"Errores del serializer: {serializer.errors}")
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MisSolicitudesView(APIView):
    def get(self, request, publicacion_id):
        publicacion = Publicacion.objects.get(pk=publicacion_id)
        serializer = PublicacionSerializer(publicacion)
        solicitudes = serializer.get_solicitudes(publicacion)
        return Response(solicitudes)
    
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class HistorialDeSolicitudesView(APIView):
    def get(self, request):
        user = request.user
        # Obtener las solicitudes basadas en las publicaciones del usuario
        solicitudes = get_solicitudes_no_espera(user)
        # Serializar las solicitudes
        serializer = SolicitudDeIntercambioSerializer(solicitudes, many=True)
        return Response(serializer.data)
    



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CancelarSolicitudView(APIView):
    def delete(self, request, solicitud_id):
        try:
            solicitud = SolicitudDeIntercambio.objects.get(id=solicitud_id)
        except SolicitudDeIntercambio.DoesNotExist:
            print("Solicitud no encontrada")
            return Response(status=HTTP_404_NOT_FOUND)

        now_local = timezone.localtime(timezone.now())
        if solicitud.fecha_del_intercambio - now_local > timedelta(hours=24):
            solicitud.delete()
            print("Solicitud eliminada de la base de datos")
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response(status=HTTP_409_CONFLICT) ##desde el front hacer un if error.status == 409 mostrar mensaje de "para cancelar un truque debe"
                                                      ## haber más de 24 horas de anticipación              