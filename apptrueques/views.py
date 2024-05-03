from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UsuarioSerializer
from django.contrib.auth.models import User

@api_view(['POST'])
def LoginView(request):
    return Response({})

@api_view(['POST'])
def RegisterView(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=serializer.data['email'])
        user.set_password(serializer.data['password'])
        user.save()
    return Response(serializer.data)

@api_view(['POST'])
def ProfileView(request):
    return Response({})
