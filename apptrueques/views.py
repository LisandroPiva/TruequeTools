from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
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
            usuario = Usuario.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password'],
                fecha_de_nacimiento=request.data['fecha_de_nacimiento'],
                sucursal_favorita=request.data['sucursal_favorita']
            )
            token, created = Token.objects.get_or_create(user=usuario)       
            response_data = {
                'token': token.key,
                'user': serializer.validated_data 
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
        print(user)
        
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
            serializer.save()  
            return Response({"publicacion": serializer.data}, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)