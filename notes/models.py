from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from django.forms import inlineformset_factory


class NoteGroup(models.Model):
    id = models.SmallAutoField(primary_key=True)
    group_name = models.CharField(max_length=25)
    password = models.CharField(max_length=25)


class CustomUser(AbstractUser):
    phone_number = models.CharField(unique=True, max_length=10, null=True, blank=True)
    note_group = models.ForeignKey(NoteGroup, on_delete=models.DO_NOTHING, null=True, blank=True)


class SNote(models.Model):
    id = models.SmallAutoField(primary_key=True)
    message = models.TextField()
    color = models.CharField(max_length=20, blank=True, null=True)
    heading = models.CharField(max_length=25, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='noteAuthor')
    is_for_group = models.BooleanField(default=False)
    to_whom = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='toWhom',
                                default=settings.AUTH_USER_MODEL)

    class Meta:
        ordering = ['datetime']


class SComment(models.Model):
    id = models.SmallAutoField(primary_key=True)
    note = models.ForeignKey(SNote, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=50)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['datetime']