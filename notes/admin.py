from django.contrib import admin

from .models import CustomUser, SNote, SComment

admin.site.register(CustomUser)
admin.site.register(SNote)
admin.site.register(SComment)
# Register your models here.
