from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
	'''User Registration Form'''
	class Meta:
		model = User
		fields = ['email','username','password1','password2']

