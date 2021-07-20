from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms import ModelForm, forms
from django import forms
from .models import NoteGroup, SNote
from django.conf import settings


class GroupCreationForm(ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput())
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = NoteGroup
        fields = ['group_name', ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        group = super(GroupCreationForm, self).save(commit=False)
        group.password = self.cleaned_data["password1"]
        if commit:
            group.save()
        return group


class GroupSignInForm(ModelForm):
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())

    class Meta:
        model = NoteGroup
        fields = ['group_id', 'password']


class MembersNoteForm(ModelForm):
    class Meta:
        model = SNote
        fields = ['heading', 'message', 'to_whom', 'is_for_group']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        if user.note_group is None:
            super(MembersNoteForm, self).__init__(*args, **kwargs)
            self.fields.pop('to_whom', None)
            self.fields.pop('is_for_group', None)
        else:
            super(MembersNoteForm, self).__init__(*args, **kwargs)
            self.fields['to_whom'].queryset = settings.AUTH_USER_MODEL.objects.filter(note_group=user.note_group)
