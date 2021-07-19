from django.urls import path
from .views import NoteAdd, NoteUpdate, MyNotesList, CustomLoginView, CustomLogoutView, NoteDelete, UserRegistration, \
    NoteGroupMembersList, group_member_delete, NoteGroupDelete, group_notes_view, NoteGroupCreate

urlpatterns = [
    path('group-create', NoteGroupCreate.as_view(), name='group-create'),
    path('group-delete/<int:pk>', NoteGroupDelete.as_view(), name='group-delete'),
    path('group-member-delete/<int:user_id>', group_member_delete, name='group-member-delete'),
    path('register/', UserRegistration.as_view(), name='register'),
    path('group-members/', NoteGroupMembersList.as_view(), name='group-members'),
    path('home/', group_notes_view, name='home'),
    path('note-delete/<int:pk>/', NoteDelete.as_view(), name='note-delete'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('add/', NoteAdd.as_view(), name='add'),
    path('edit/<int:pk>/', NoteUpdate.as_view(), name='edit'),
    path('', MyNotesList.as_view(), name='notes'),
]
