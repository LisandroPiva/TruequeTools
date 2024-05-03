from django.shortcuts import render
from rest_framework.response import  response
from rest_framework.decorators import api_view

@api_view(['POST'])
def login(request):
    return response({})

@api_view(['POST'])
def register(request):
    return response({})

@api_view(['POST'])
def profile(request):
    return response({})
