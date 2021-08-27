from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class AdminCustomUser(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number']
    search_fields = ['username', 'email']

