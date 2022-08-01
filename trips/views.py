from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserTokenSerializer,UserCreateSerializer
from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView
)
# Create your views here.

# Auth Views 

class UserTokenApiView(TokenObtainPairView):
    serializer_class= UserTokenSerializer

class Register(CreateAPIView):
    serializer_class = UserCreateSerializer