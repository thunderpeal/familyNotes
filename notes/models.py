# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

from django.forms import inlineformset_factory

#create own user-class

class UserAccount(models.Model):
    id = models.SmallAutoField(primary_key=True)
    login = models.CharField(unique=True, max_length=25)
    password = models.CharField(unique=True, max_length=25)
    nickname = models.CharField(unique=True, max_length=25)
    email = models.CharField(unique=True, max_length=50)
    phonenumber = models.CharField(unique=True, max_length=10)

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'user_account'


class SNote(models.Model):
    id = models.SmallAutoField(primary_key=True)
    message = models.TextField()
    color = models.CharField(max_length=20, blank=True, null=True)
    heading = models.CharField(max_length=25, blank=True, null=True)
    datetime = models.DateTimeField()
    author = models.ForeignKey('UserAccount', models.DO_NOTHING, db_column='author', related_name='noteAuthor')
    to_whom = models.ForeignKey('UserAccount', models.DO_NOTHING, db_column='to_whom', blank=True, null=True,
                                related_name='toWhom')

    class Meta:
        db_table = 's_note'


class SComment(models.Model):
    id = models.SmallAutoField(primary_key=True)
    note = models.ForeignKey('SNote', db_column='note', on_delete=models.CASCADE)
    author = models.ForeignKey('UserAccount', models.DO_NOTHING, db_column='author')
    message = models.CharField(max_length=50)
    datetime = models.DateTimeField()

    class Meta:
        db_table = 's_comment'



