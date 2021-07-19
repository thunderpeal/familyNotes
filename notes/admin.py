from django.contrib import admin

from .models import CustomUser, SNote, SComment, NoteGroup

admin.site.register(CustomUser)
admin.site.register(NoteGroup)
admin.site.register(SNote)
admin.site.register(SComment)
# Register your models here.
