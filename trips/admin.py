from django.contrib import admin
from .models import  Question, Trip, Profile

# Register your models here.
admin.site.register(Trip)
admin.site.register(Profile)
admin.site.register(Question)
