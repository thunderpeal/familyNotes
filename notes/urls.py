from django.urls import path
from django.views.generic import TemplateView
from .views import NoteCreate, NoteUpdate, NotesLists, NoteDelete, GroupMembersList, group_member_delete, \
    GroupDelete, GroupCreate, GroupLoginView, kostyl, CustomTemplateView

urlpatterns = [
    path('settings/', CustomTemplateView.as_view(), name='settings'),
    path('group-create', GroupCreate.as_view(), name='group-create'),
    path('group-delete/<int:pk>', GroupDelete.as_view(), name='group-delete'),
    path('group-member-delete/<int:user_id>', group_member_delete, name='group-member-delete'),
    path('group-management/', GroupMembersList.as_view(), name='group-management'),
    path('group-login/', GroupLoginView.as_view(), name='group-login'),
    path('note-delete/<int:pk>/', NoteDelete.as_view(), name='note-delete'),
    path('note-create/', NoteCreate.as_view(), name='add'),
    path('note-edit/<int:pk>/', NoteUpdate.as_view(), name='edit'),
    path('notes/', NotesLists.as_view(), name='notes'),
    path('', kostyl),
]
