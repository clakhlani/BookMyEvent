from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
	if request.method=="POST":
		form =RegistrationForm(request.POST)
		if form.is_valid():
			email=form.cleaned_data['email']
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f'Account created for {username}')
			return redirect('login_page')
	else:
		form=RegistrationForm()
	return render(request,'user/register.html',{'form':form})


@login_required(login_url='login_page')
def logout_user(request):
	logout(request)
	return redirect('login_page')