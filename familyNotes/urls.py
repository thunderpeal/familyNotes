from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('general/', include('basic.urls')),
    path('', include('notes.urls'), name='notes'),
]
