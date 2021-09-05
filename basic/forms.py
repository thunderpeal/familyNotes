from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Username', 'name': 'username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password', 'name': 'pass'}))


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Username', 'name': 'username'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password', 'name': 'pass'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password Confirmation', 'name': 'pass'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'phone_number']
