import django.forms as forms
from .views import SNote

class NoteForm(forms.ModelForm):
    class Meta:
        model = SNote
        fields = "__all__"
        widgets = {'author': forms.HiddenInput}

