from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
urlpatterns = [
    path('register/', views.register,name='register'),
    path('login/', LoginView.as_view(template_name='user/login.html'),name='login_page'),
    path('logout/', views.logout_user, name='logout'),

    

]