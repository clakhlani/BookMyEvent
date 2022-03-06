from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
	'''Adding email field to inbuilt Abstract user.'''
	email=models.EmailField(unique=True)
	
