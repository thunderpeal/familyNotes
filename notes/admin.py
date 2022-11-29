from django.contrib import admin

from .models import SNote, SComment, Group, Membership, Notification


@admin.register(Group)
class AdminNoteGroup(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id']


@admin.register(SNote)
class AdminSNote(admin.ModelAdmin):
    search_fields = ['to_whom', 'author']
    list_filter = ['to_whom', 'author', 'datetime']


@admin.register(Membership)
class AdminMembership(admin.ModelAdmin):
    search_fields = ['user', 'group']
    list_filter = ['user', 'group', 'ban']


@admin.register(Notification)
class AdminMembership(admin.ModelAdmin):
    search_fields = ['user', 'datetime']
    list_filter = ['user', 'datetime']


admin.site.register(SComment)
