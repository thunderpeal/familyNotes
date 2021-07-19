from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import CustomUser, NoteGroup


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'phone_number')


class GroupSignInForm(ModelForm):
    class Meta:
        model = NoteGroup
        fields = ('id', 'group_name', 'password')
