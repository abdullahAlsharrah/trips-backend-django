from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    gender_choices = [
        ("male", "male"),
        ("female", "female"),
    ]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=10, choices=gender_choices, default="male")
    birth_date = models.DateField(default="1990-01-01")
    image = models.ImageField(upload_to="profile/",default="" )
    bio = models.TextField(default="")
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user.id)+" "+ self.user.username

class Trip(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True,related_name="trips")   
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to="trips/",default="")

    def __str__(self):
        return self.title