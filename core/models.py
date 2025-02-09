from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here to extend user model
class User(AbstractUser):
    # redefined email field
    email = models.EmailField(unique=True)