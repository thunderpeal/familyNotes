from django.contrib import admin

from .models import SNote, SComment, Group, Membership


@admin.register(Group)
class AdminNoteGroup(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id']


@admin.register(SNote)
class AdminSNote(admin.ModelAdmin):
    search_fields = ['to_whom', 'author']
    list_filter = ['to_whom', 'author', 'datetime']


admin.site.register(SComment)
admin.site.register(Membership)

