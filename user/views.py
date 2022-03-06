from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

'''This file is for validating user registration and sign in'''




# Create your views here.
def register(request):
	'''View that validates user registration checks if same username or email exists.'''
	if request.method=="POST":
		form =RegistrationForm(request.POST)                               #Getting the registration formn submitted
		if form.is_valid():                                                #Validating form
			email=form.cleaned_data['email']										
			form.save()                                                    #Saving form. New user will be created.
			username = form.cleaned_data.get('username')
			messages.success(request,f'Account created for {username}') 
			return redirect('login_page')                                  #Redirect to login page.Message will be displayed.
	else:
		form=RegistrationForm()
	return render(request,'user/register.html',{'form':form})


@login_required(login_url='login_page')
def logout_user(request):
	'''View to logout of the session.'''
	logout(request)
	return redirect('login_page')                                          #On logout redirect to login page.