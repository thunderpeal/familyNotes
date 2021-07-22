from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class AdminCustomUser(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'note_group']
    search_fields = ['username', 'note_group', 'email']
    list_filter = ['note_group']
