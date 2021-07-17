
from django.urls import path, include
from . import views
urlpatterns = [
    path('add', views.NoteAdd.as_view(), name='add'),
    path('', views.IndexView.as_view(), name='notes'),
]