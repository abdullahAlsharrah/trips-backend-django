import profile
from pyexpat import model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils import trips as t,username
from .models import  Profile, Trip
## for adding more details such as username in the token

User = get_user_model()

class UserTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)


    class Meta:
        model = User
        fields = ['username', 'password','refresh', 'access']
    def create(self, validated_data):
        new_user = User(**validated_data)
        new_user.set_password(new_user.password)
        new_user.save()
        token = UserTokenSerializer.get_token(new_user)
        validated_data['refresh'] = str(token)
        validated_data['access'] = str(token.access_token)

        # create profile
        try:
            gender=self.context['request'].data["gender"]
            birth_date=self.context['request'].data["birth_date"]
            image=self.context['request'].data['image']
        except:
            gender=""
            birth_date="1990-01-01"
            image=""

        Profile.objects.create(
            user = new_user,
            gender=gender,
            birth_date=birth_date,
            image=image
            # etc... 
        )
        # data = {'profile': profile ,'access':validated_data['access'], 'refresh':validated_data['refresh'],'username':validated_data['username'] }

        return validated_data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['username','id']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields=['user']

class TripSerilizer(serializers.ModelSerializer):
    # profile=ProfileSerializer()
    owner = serializers.SerializerMethodField()
    class Meta:
        model= Trip
        fields= '__all__'

    def get_owner(self, obj):
        return username(obj.get_owner())

class FavoriteTripSerilizer(serializers.ModelSerializer):
    class Meta:
        model= Trip
        fields= ['favorite']
    def update(self, instance, validated_data):
        if (instance.favorite.filter(user__id=self.context['request'].user.id).exists()):
            instance.favorite.remove(self.context['request'].user.id)
        else:
             instance.favorite.add(self.context['request'].user.id)
        return instance



class TripEditSerilizer(serializers.ModelSerializer):
    class Meta:
        model= Trip
        fields= ['title','description','image']

class CreateTripSerilizer(serializers.ModelSerializer):
    class Meta:
        model= Trip
        fields= ['title','description','image']

class ProfileViewSerilizer(serializers.ModelSerializer):
    trips = TripSerilizer(many=True,read_only=True)
    favorite =serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    class Meta:
        model= Profile
        fields= '__all__'

    def get_username(self, obj):
        return obj.get_username()

    def get_favorite(self, obj):
        trips = Trip.objects.all()
        # print(trips)
        # _trips = trips.objects.filter(favorite__in= 2)
        return t(obj.my_favorite_list(trips))
  


