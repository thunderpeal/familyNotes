from django.contrib import admin

from .models import SNote, SComment, NoteGroup

admin.site.register(NoteGroup)
admin.site.register(SNote)
admin.site.register(SComment)
