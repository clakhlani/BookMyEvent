from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth import logout
# Create your views here.
def register(request):
	if request.method=="POST":
		form =RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f'Account created for {username}')
			print
			return redirect('login_page')
	else:
		form=RegistrationForm()
	return render(request,'user/register.html',{'form':form})



def logout_user(request):
	logout(request)
	return redirect('login_page')