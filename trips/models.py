from django.db import models
from django.contrib.auth.models import User


# Create your models here.



class Profile(models.Model):
    gender_choices = [
        ("Gender", "Gender"),
        ("male", "male"),
        ("female", "female"),
    ]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=10, choices=gender_choices, default="Gender")
    birth_date = models.DateField(default="1990-01-01")
    image = models.ImageField(upload_to="profile/",default="")
    bio = models.TextField(default="To change your bio, edit your profile!")
    date_joined = models.DateField(auto_now_add=True)
    first_name = models.CharField(max_length=10, default="")
    last_name = models.CharField(max_length=10, default="")
    # favorite_lists = models.OneToOneField(Favorite, on_delete=models.CASCADE,null=True )   

    def get_username(self):
        return self.user.username

    def my_favorite_list(self, trips):
        favorite_list = []
        for trip in trips:
            if(trip.favorite.filter(user__id=self.user.id)):
                favorite_list.append(trip)
        my_favorite_list = list(set(favorite_list))
        return my_favorite_list

    def __str__(self):
        return self.user.username

class Trip(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True,related_name="trips")   
    favorite = models.ManyToManyField(Profile, default=None,blank=True,related_name="favorites")   
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to="trips/",default="")

    def get_owner(self):
        print(self.profile)
        return self.profile

    def __str__(self):
        return self.title


 
