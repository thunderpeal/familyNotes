from django.urls import path
from django.views.generic import TemplateView
from .views import NoteCreate, NoteUpdate, NotesLists, NoteDelete, GroupManagement, group_member_delete, \
    GroupDelete, GroupCreate, GroupLoginView, kostyl, CustomTemplateView, BanManagement, RestoreMember

urlpatterns = [
    path('settings/', CustomTemplateView.as_view(), name='settings'),
    path('group-create', GroupCreate.as_view(), name='group-create'),
    path('group-delete/<int:pk>', GroupDelete.as_view(), name='group-delete'),
    path('group-member-delete/<int:group_id>/<int:user_id>', group_member_delete, name='group-member-delete'),
    path('group-management/<int:group_id>/ban-management/', BanManagement.as_view(), name='ban-management'),
    path('group-management/<int:group_id>/restore-members/<int:user_id>', RestoreMember.as_view(), name='restore-member'),
    path('group-management/', GroupManagement.as_view(), name='group-management'),


    path('group-login/', GroupLoginView.as_view(), name='group-login'),
    path('note-delete/<int:pk>/', NoteDelete.as_view(), name='note-delete'),
    path('note-create/', NoteCreate.as_view(), name='add'),
    path('note-edit/<int:pk>/', NoteUpdate.as_view(), name='edit'),
    path('notes/', NotesLists.as_view(), name='notes'),
    path('', kostyl),
]
