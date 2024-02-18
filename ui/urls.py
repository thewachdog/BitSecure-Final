# myapp/urls.py
from django.contrib.auth import views
from django.urls import path
from .views import *
from .forms import CustomUserLoginForm
from django.conf.urls.static import static

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/',views.LoginView.as_view(
            template_name="login.html",
            authentication_form=CustomUserLoginForm
            ), name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home'),

    path('upload/', upload_video, name='upload'),
    path('decode/', decode_video, name='decode'),

    path('videos/', videos, name='videos'),
    path('videos/<str:vidName>', player, name='player'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
