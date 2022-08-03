from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView

from trips.models import Profile, Trip
from .serializers import  CreateTripSerilizer, ProfileViewSerilizer, TripSerilizer, UserTokenSerializer,UserCreateSerializer
from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from .permissions import  IsOwner,IsTripOwner
# Create your views here.

# Auth Views 

class UserTokenApiView(TokenObtainPairView):
    serializer_class= UserTokenSerializer

class Register(CreateAPIView):
    serializer_class = UserCreateSerializer

# Trips

class CreateTrip(CreateAPIView):
    serializer_class = CreateTripSerilizer
    permission_classes = [IsAuthenticated,]
    def perform_create(self, serializer):
        serializer.save(profile = self.request.user.profile)

class TripList(ListAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerilizer

class UserTripList(ListAPIView):
    serializer_class = TripSerilizer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return Trip.objects.filter(profile=self.request.user.profile)


class TripDetails(RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerilizer
    lookup_field = 'id'
    lookup_url_kwarg='trip_id'

class UpdateDeleteTrip(RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerilizer
    permission_classes = [IsAuthenticated,IsTripOwner,]
    lookup_field = 'id'
    lookup_url_kwarg='trip_id'

class DeleteTrip(DestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerilizer
    permission_classes = [IsAuthenticated,IsTripOwner,]
    lookup_field = 'id'
    lookup_url_kwarg='trip_id'

# Profile

class UpdateProfile(RetrieveUpdateAPIView):
    serializer_class = ProfileViewSerilizer
    permission_classes = [IsAuthenticated,IsOwner]
    def get_object(self):
         return self.request.user.profile

class ProfileView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileViewSerilizer
    lookup_field = 'user__id'
    lookup_url_kwarg='profile_id'
   