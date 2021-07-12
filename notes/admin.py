from django.contrib import admin

from .models import UserAccount, SNote, SComment

admin.site.register(UserAccount)
admin.site.register(SNote)
admin.site.register(SComment)
# Register your models here.
