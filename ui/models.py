# myapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any additional fields here
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='encoded/')
    url = models.CharField(default = '', max_length=100)
