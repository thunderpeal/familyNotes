from django.urls import path
from .views import NoteAdd, NoteUpdate, MyNotesList, NoteDelete, NoteGroupMembersList, group_member_delete, \
    NoteGroupDelete, group_notes_view, NoteGroupCreate, about

urlpatterns = [
    path('settings/', about, name='settings'),
    path('group-create', NoteGroupCreate.as_view(), name='group-create'),
    path('group-delete/<int:pk>', NoteGroupDelete.as_view(), name='group-delete'),
    path('group-member-delete/<int:user_id>', group_member_delete, name='group-member-delete'),
    path('group-members/', NoteGroupMembersList.as_view(), name='group-members'),
    path('group-notes/', group_notes_view, name='home'),
    path('note-delete/<int:pk>/', NoteDelete.as_view(), name='note-delete'),
    path('add/', NoteAdd.as_view(), name='add'),
    path('edit/<int:pk>/', NoteUpdate.as_view(), name='edit'),
    path('my-notes/', MyNotesList.as_view(), name='my-notes'),
]
