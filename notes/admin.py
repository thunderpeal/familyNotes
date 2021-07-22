from django.contrib import admin

from .models import SNote, SComment, NoteGroup


@admin.register(NoteGroup)
class AdminNoteGroup(admin.ModelAdmin):
    list_display = ['id', 'group_name']
    search_fields = ['id']


@admin.register(SNote)
class AdminSNote(admin.ModelAdmin):
    search_fields = ['to_whom', 'author']
    list_filter = ['to_whom', 'author', 'datetime']


admin.site.register(SComment)
