# myapp/urls.py
from django.contrib.auth import views
from django.urls import path
from .views import *
from .forms import CustomUserLoginForm

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/',views.LoginView.as_view(
            template_name="login.html",
            authentication_form=CustomUserLoginForm
            ), name='login'),
            # , login_view
    path('logout/', logout_view, name='logout'),
    path('', home, name='home')
    # Add other URLs as needed
]
