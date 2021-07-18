from django.urls import path, include
from .views import NoteAdd, NoteUpdate, NotesList, CustomLoginView, CustomLogoutView, NoteDelete, UserRegistration

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('note-delete/<int:pk>/', NoteDelete.as_view(), name='note-delete'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('add/', NoteAdd.as_view(), name='add'),
    path('edit/<int:pk>/', NoteUpdate.as_view(), name='edit'),
    path('', NotesList.as_view(), name='notes'),
]