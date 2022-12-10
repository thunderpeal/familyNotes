from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput, Textarea


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Username', 'name': 'username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password', 'name': 'pass'}))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Username', 'name': 'username'}))
    email = forms.CharField(widget=EmailInput(attrs={'placeholder': 'Email', 'name': 'email'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password', 'name': 'pass'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password Confirmation', 'name': 'pass'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class AccountSettings(UserChangeForm):
    username = forms.CharField(
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'name': 'email'}), disabled=True)
    email = forms.EmailField(
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'email', 'name': 'email'}), disabled=True)
    first_name = forms.CharField(
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'first name', 'name': 'first_name'}),
        required=False)
    last_name = forms.CharField(
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'last name', 'name': 'last_name'}),
        required=False)
    bio = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'bio', 'name': 'bio', 'rows': '5'}),
                          required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'bio']
