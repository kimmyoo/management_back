from django.contrib.auth.models import AbstractUser
from django.db import models
# from rest_framework import APIView


# Create your models here.
class User(AbstractUser):
    email = models.CharField(max_length=225, unique=True)
    username = models.CharField(max_length=225, unique=True)
    password = models.CharField(max_length=225)

    USERNAME_FIELD= 'username'
    REQUIRED_FIELDS = ['email']