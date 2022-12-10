from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='pics', null=True, blank=True)
    phone_number = models.CharField(unique=True, max_length=10, null=True, blank=True)
    bio = models.TextField(unique=False, null=True, blank=True)


