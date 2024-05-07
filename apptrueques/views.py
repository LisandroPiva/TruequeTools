from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.authtoken.models import Token
from .models import Usuario
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes

@permission_classes([AllowAny])
class RegisterView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            sucursal = get_object_or_404(Sucursal, pk=request.data['sucursal_favorita'])
            usuario = Usuario.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password'],
                fecha_de_nacimiento=request.data['fecha_de_nacimiento'],
                sucursal_favorita=sucursal  
            )
            token, created = Token.objects.get_or_create(user=usuario)
            response_data = {
                'token': token.key,
                'user': serializer.validated_data,
                'sucursal favorita':sucursal.nombre
            }
            
            return Response(response_data, status=HTTP_201_CREATED)
        else:
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
        request.data['usuario_propietario'] = request.user.id
        serializer = PublicacionSerializer(data=request.data)
        if serializer.is_valid():
            request.data['estado'] = 'PUBLICADA'
            serializer.save()  
            return Response({"publicacion publicada con éxito": serializer.data}, status=HTTP_201_CREATED)
        else:
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
            return Response({"detail": "Comentario publicado con éxito", "comentario": serializer.data}, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CreateReplyView(APIView):
    def post(self, request, publicacion_id, comentario_id):
        try:
            publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
            comentario_original = get_object_or_404(Comentario, pk=comentario_id)
        except Comentario.DoesNotExist:
            return Response({"detail": "El comentario que deseas responder ya no está disponible"}, status=HTTP_404_NOT_FOUND)
        
        request.data['usuario_propietario'] = request.user.id
        request.data['comentario_original'] = comentario_id
        serializer = ComentarioRespuestaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response({"detail": "Respuesta enviada con éxito", "respuesta": serializer.data}, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PostDetailView(APIView):
    def get(self, request, publicacion_id):
        try:
            publicacion = Publicacion.objects.get(pk=publicacion_id)
            serializer = PublicacionSerializer(publicacion)
            return Response(serializer.data, status=HTTP_200_OK)
        except Publicacion.DoesNotExist:
            raise NotFound("La publicación no existe")
    
