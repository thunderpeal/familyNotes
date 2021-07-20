from django.db import models
from notes.models import NoteGroup
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(unique=True, max_length=10, null=True, blank=True)
    note_group = models.ForeignKey(NoteGroup, on_delete=models.DO_NOTHING, null=True, blank=True)
    group_admin = models.BooleanField(default=False)
