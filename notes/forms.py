from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import Group, SNote
from basic.models import CustomUser
from django.db.models import Q


class GroupCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput())
    password2 = forms.CharField(label=_("Password Again"), widget=forms.PasswordInput())

    class Meta:
        model = Group
        fields = ['name', ]

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


class NoteForm(forms.ModelForm):
    class Meta:
        model = SNote
        fields = ['heading', 'message', 'group', 'to_whom']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(NoteForm, self).__init__(*args, **kwargs)
        users_groups = user.members_groups.all()
        if not users_groups:
            self.fields.pop('to_whom', None)
            self.fields.pop('group', None)
        else:
            self.fields['group'].queryset = users_groups
            self.fields['to_whom'].queryset = CustomUser.objects.none()
            for group in users_groups:
                members = CustomUser.objects.filter(group_members__group=group, group_members__ban=False)
                members = members.exclude(id=user.id)
                self.fields['to_whom'].queryset = self.fields['to_whom'].queryset.union(members)
            if not self.fields['to_whom'].queryset:
                self.fields.pop('to_whom')


class NoteFormPersonal(forms.ModelForm):
    class Meta:
        model = SNote
        fields = ['heading', 'message', 'to_whom']
