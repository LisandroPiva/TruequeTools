from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_406_NOT_ACCEPTABLE, HTTP_409_CONFLICT
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.authtoken.models import Token
from .models import Usuario
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from datetime import datetime
from rest_framework.exceptions import ValidationError


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
            serializer.save(usuario_propietario=request.user)  
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CreateCommentView(APIView):
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
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CreateReplyView(APIView):
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

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PostDetailView(APIView):
    def get(self, request, publicacion_id):
        print(request)
        print("AAAAAAAAA", publicacion_id)
        try:
            publicacion = Publicacion.objects.get(pk=publicacion_id)
            serializer = PublicacionSerializer(publicacion)
            return Response(serializer.data, status=HTTP_200_OK)
        except Publicacion.DoesNotExist:
            return Response({"detail": "La publicación que deseas ver no está disponible"}, status=HTTP_404_NOT_FOUND)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserInfoView(APIView):
     def get(self, request):
        user = request.user
        serializer = UsuarioSerializer(user)
        return Response(serializer.data)

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