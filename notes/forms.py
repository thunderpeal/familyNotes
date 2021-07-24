from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms
from .models import NoteGroup, SNote
from basic.models import CustomUser
from django.db.models import Q


class GroupCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput())
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput(),
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


class MembersNoteForm(forms.ModelForm):
    class Meta:
        model = SNote
        fields = ['heading', 'message', 'to_whom', 'is_for_group']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MembersNoteForm, self).__init__(*args, **kwargs)
        if user.note_group is None:
            self.fields.pop('to_whom', None)
            self.fields.pop('is_for_group', None)
        else:
            to_members = CustomUser.objects.filter(Q(note_group=user.note_group) & ~Q(username=user.username))
            if to_members:
                self.fields['to_whom'].queryset = to_members
            else:
                self.fields.pop('to_whom')
