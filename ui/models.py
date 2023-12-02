# myapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any additional fields here
    # email = models.EmailField(unique=True)
    pass
