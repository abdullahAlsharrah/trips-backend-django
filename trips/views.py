from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView

from trips.models import  Profile, Question, Trip
from .serializers import  CreateTripSerilizer, DeleteTripSerilizer, FavoriteTripSerilizer, PostQuestionSerilizer, ProfileViewSerilizer, ReplyQuestionSerilizer, TripEditSerilizer, TripSerilizer, UserTokenSerializer,UserCreateSerializer, WantToGoTripSerilizer
from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from .permissions import  IsOwner,IsTripOwner, isOwnerOfTrip
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

class MyFavoriteTripList(ListAPIView):
    serializer_class = TripSerilizer
    permission_classes = [IsAuthenticated,]
    def get_queryset(self):
        return Trip.objects.filter(favorite__in=str(self.request.user.id))

class AddFavoriteTrip(RetrieveUpdateAPIView):
    queryset = Trip.objects.all()
    serializer_class = FavoriteTripSerilizer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'
    lookup_url_kwarg='trip_id'

class WantToGoTrip(RetrieveUpdateAPIView):
    queryset = Trip.objects.all()
    serializer_class = WantToGoTripSerilizer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'
    lookup_url_kwarg='trip_id'
       
         


class TripDetails(RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerilizer
    lookup_field = 'id'
    lookup_url_kwarg='trip_id'

class UpdateDeleteTrip(RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripEditSerilizer
    permission_classes = [IsAuthenticated,IsTripOwner,]
    lookup_field = 'id'
    lookup_url_kwarg='trip_id'

class DeleteTrip(DestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = DeleteTripSerilizer
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
   
#questions 

class PostQuestion(CreateAPIView):
    serializer_class = PostQuestionSerilizer
    permission_classes = [IsAuthenticated,]
    def perform_create(self, serializer):
        query = self.request.GET
        print(query['trip_id'])
        trip = Trip.objects.get(id = int(query['trip_id']))
        serializer.save(profile = self.request.user.profile , trip = trip) 
        
class ReplyOnQuestion(CreateAPIView):
    serializer_class = ReplyQuestionSerilizer
    permission_classes = [IsAuthenticated,isOwnerOfTrip]
    def perform_create(self, serializer):
        query = self.request.GET
        question = Question.objects.get(id = int(query['question_id']))
        serializer.save(profile = self.request.user.profile , question = question) 