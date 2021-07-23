from django.urls import path
from django.views.generic import TemplateView
from .views import NoteCreate, NoteUpdate, MyNotesList, NoteDelete, NoteGroupMembersList, group_member_delete, \
    NoteGroupDelete, NoteGroupCreate, GroupNotesView, kostyl

urlpatterns = [
    path('settings/', TemplateView.as_view(template_name='notes/settings.html'), name='settings'),
    path('group-create', NoteGroupCreate.as_view(), name='group-create'),
    path('group-delete/<int:pk>', NoteGroupDelete.as_view(), name='group-delete'),
    path('group-member-delete/<int:user_id>', group_member_delete, name='group-member-delete'),
    path('group-members/', NoteGroupMembersList.as_view(), name='group-members'),
    path('group-notes/', GroupNotesView.as_view(), name='home'),
    path('note-delete/<int:pk>/', NoteDelete.as_view(), name='note-delete'),
    path('note-create/', NoteCreate.as_view(), name='add'),
    path('note-edit/<int:pk>/', NoteUpdate.as_view(), name='edit'),
    path('my-notes/', MyNotesList.as_view(), name='my-notes'),
    path('', kostyl),
]
