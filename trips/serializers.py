import profile
from pyexpat import model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils import trips as t,username,owner_image
from .models import  Profile, Question, Reply, Trip
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
        fields=['image']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields='__all__'


class DeleteTripSerilizer(serializers.ModelSerializer):
    class Meta:
        model= Trip
        fields= ['title']

class TripSerilizer(serializers.ModelSerializer):
    questions =serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    owner_image = serializers.SerializerMethodField()
    class Meta:
        model= Trip
        fields= ['id','owner','owner_image','title','description','image','profile','favorite','want_to','questions']

    def get_owner(self, obj):
        return username(obj.get_owner())

    def get_owner_image(self, obj):
        return owner_image(obj.get_owner_image())

    def get_questions(self, obj):
        questions = Question.objects.filter(trip__id=obj.id).values('id','replies','trip','profile','text',)
        for question in questions:
            question['replies'] = Reply.objects.filter(question__id=question['id']).values()
            profile= Profile.objects.filter(user=question['profile']).values()[0]
            question['image']= "http://10.0.2.2:8000/media/" + profile['image']
            question['profile']= profile['user_id']
           
        return questions
    

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

class WantToGoTripSerilizer(serializers.ModelSerializer):
    class Meta:
        model= Trip
        fields= ['want_to']
    def update(self, instance, validated_data):
        if (instance.want_to.filter(user__id=self.context['request'].user.id).exists()):
            instance.want_to.remove(self.context['request'].user.id)
        else:
             instance.want_to.add(self.context['request'].user.id)
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
    want_to =serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    class Meta:
        model= Profile
        fields= '__all__'

    def get_username(self, obj):
        return obj.get_username()

    def get_favorite(self, obj):
        trips = Trip.objects.all()
        return t(obj.my_favorite_list(trips))

    def get_want_to(self, obj):
        trips = Trip.objects.all()
        return t(obj.my_want_to_list(trips))

class PostQuestionSerilizer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields='__all__'

class ReplyQuestionSerilizer(serializers.ModelSerializer):
    class Meta:
        model=Reply
        fields='__all__'



    
  


