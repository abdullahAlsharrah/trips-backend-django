from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Profile
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
        Profile.objects.create(
            user = new_user,
            gender=self.context['request'].data["gender"],
            birth_date=self.context['request'].data["birth_date"],
            image=self.context['request'].data['image'],
            # etc... 
        )
        # data = {'profile': profile ,'access':validated_data['access'], 'refresh':validated_data['refresh'],'username':validated_data['username'] }

        return validated_data
