import datetime
import random
from django.template.defaulttags import register

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import SNote, Group, Membership, Notification
from basic.models import CustomUser
from django.db.models import Q

from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import NoteForm, GroupCreationForm, NoteFormPersonal, ColorForm, GroupFormName, GroupFormPass

import requests


class NotesLists(LoginRequiredMixin, View):
    """
    This view prepares data to notes page: personal notes, all notes from user's groups.
    Personal notes go to context as 'my_notes_list', groups' notes are put into 'group_notes_list' dictionary.
    """
    def get(self, request):
        context = {}
        my_notes_list = SNote.objects.filter((Q(to_whom=self.request.user) | Q(to_whom=None, author=self.request.user))
                                             & Q(group=None))
        context['group_notes_list'] = {'my_notes_list': my_notes_list}
        groups = self.request.user.members_groups.all()

        if groups:
            context['groups_available'] = True
            group_notes = {}
            memberships = {}
            for group in groups:
                notes_per_g = SNote.objects.filter(Q(group=group))
                group_notes[group] = notes_per_g
                membership = Membership.objects.get(user=self.request.user, group=group)
                memberships[group] = membership

            context['group_notes_list'].update(group_notes)
            context['memberships'] = memberships
        notifications_length = Notification.objects.filter((Q(user=self.request.user) & Q(is_read=False))).count()
        context['notifications_length'] = notifications_length
        return render(request, 'notes/notes.html', context=context)


class NotificationList(LoginRequiredMixin, ListView):
    """
    """
    model = Notification
    paginate_by = 100
    template_name = 'notes/notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.datetime.now()
        user_notifications_new = Notification.objects.filter((Q(user=self.request.user) & Q(is_read=False)))
        user_notifications_old = Notification.objects.filter((Q(user=self.request.user) & Q(is_read=True)))
        context['types'] = ['new', 'old']
        notifications_length = user_notifications_new.count()
        context['notifications'] = {'new': user_notifications_new, 'old': user_notifications_old}
        context['notifications_length'] = notifications_length
        for notification in context['notifications']['new']:
            notification.is_read = True
            notification.save()
        return context


class NoteCreate(LoginRequiredMixin, CreateView):
    template_name = 'notes/note_create.html'
    success_url = reverse_lazy('notes')
    form_class = NoteForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NoteCreate, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(NoteCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class NoteCreatePersonal(LoginRequiredMixin, CreateView):
    """
    This view is used to send a note to a certain person (from one of the user's groups).
    It will be put in 'my_notes_list' list in NotesLists view.
    """
    template_name = 'notes/note_create_personal.html'
    success_url = reverse_lazy('notes')
    form_class = NoteFormPersonal

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.to_whom = CustomUser.objects.get(id=self.kwargs.pop('member_id'))
        return super(NoteCreatePersonal, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = CustomUser.objects.get(id=self.kwargs.pop('member_id'))
        context['member'] = member

        return context


class NoteUpdate(LoginRequiredMixin, UpdateView):
    """
    This view is used to update certain note's data: message, group or receiver.
    If user is not present in any group then it's only available to update message field.

    Heading field is currently unused in ui.
    """
    model = SNote
    fields = ['message', 'group', 'to_whom']
    success_url = reverse_lazy('notes')

    def get_form_class(self):
        if not self.request.user.members_groups.all():
            self.fields = ['message', ]
        return super(NoteUpdate, self).get_form_class()


class NoteDelete(LoginRequiredMixin, DeleteView):
    model = SNote
    context_object_name = 'note'
    success_url = reverse_lazy('notes')


class GroupManagement(LoginRequiredMixin, View):
    """
    This view is used to manage all the user's groups. Here he can enter or create new ones (via links to other views),
    view certain group's information: name, id (needed to invite new members), current members of the group.
    """
    def get(self, request, *args, **kwargs):
        groups = Group.objects.filter(group_members__user=request.user, group_members__ban=False)
        if not groups:
            return redirect('group-login')
        groups_members = {}
        groups_colors = {}
        for group in groups:
            members = CustomUser.objects.filter(group_members__group=group, group_members__ban=False)
            membership = Membership.objects.get(group=group, user=self.request.user)
            groups_members[group] = members
            groups_colors[group.name] = "#" + str(membership.color)
        context = {'groups_members': groups_members, 'groups': groups, 'groups_colors': groups_colors}
        return render(request, 'notes/group_management.html', context=context)


@login_required
def group_member_delete(request, group_id, user_id):
    """
    This view is used to delete certain user of a group. It's also used to leave group. If user to leave is admin
    of the group, then new admin will be chosen from left users of group. If there are no left users, then group
    is deleted with no saving data (notes, members and etc).
    """
    user = CustomUser.objects.get(id=user_id)
    group = Group.objects.get(id=group_id)

    if user != request.user:
        membership = Membership.objects.get(user=user, group=group)
        membership.ban = True
        membership.save()
    else:
        membership = Membership.objects.get(user=user, group=group)
        membership.delete()

    if group.admin == user:
        members = group.members.all()
        if members:
            group.admin = members[0]
            group.save()
        else:
            group.delete()
    return redirect('group-management')


class BanManagement(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        group = Group.objects.get(id=kwargs['group_id'])
        banned_members = CustomUser.objects.filter(group_members__group=group, group_members__ban=True)
        context = {'banned_members': banned_members, 'group': group}
        return render(request, 'notes/ban-management.html', context=context)


class RestoreMember(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        group = Group.objects.get(id=kwargs['group_id'])
        user = CustomUser.objects.get(id=kwargs['user_id'])
        membership = Membership.objects.get(user=user, group=group)
        membership.ban = False
        membership.save()

        return redirect('ban-management', group_id=group.id)


class GroupDelete(LoginRequiredMixin, DeleteView):
    """
    This view is used to delete note group. delete method is modified so that we also delete every
    connection between users and this group (they have many-to-many relationship through the third model).
    Also all notes related to this group are also deleted.
    """
    model = Group
    context_object_name = 'group'
    success_url = reverse_lazy('group-management')

    def delete(self, request, *args, **kwargs):
        memberships = Membership.objects.filter(group=self.get_object())
        notes = SNote.objects.filter(group=self.get_object())
        for membership in memberships:
            membership.delete()
        for note in notes:
            note.delete()

        return super(GroupDelete, self).delete(request, *args, **kwargs)


class GroupLoginView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.members_groups.all():
            redirect('group-management')
        return render(request, 'notes/group_login.html')

    def post(self, request, *args, **kwargs):
        group = Group.objects.filter(id=request.POST['group_id'])
        failure = "Need password"
        if group:
            membership = Membership.objects.filter(user=request.user, group=group[0])

            if membership:
                if membership[0].ban:
                    failure = "You've been banned from this group."
            elif group[0].password == request.POST['password']:
                group[0].members.add(request.user)
                return redirect('group-management')
            else:
                failure = 'Wrong password.'
        else:
            failure = 'There is no group with given id.'

        context = {'failure': failure, 'searched_id': request.POST['group_id']}
        return render(request, 'notes/group_login.html', context=context)


class GroupCreate(LoginRequiredMixin, CreateView):
    form_class = GroupCreationForm
    template_name = 'notes/group_registration.html'
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        form.instance.admin = self.request.user
        response = super(GroupCreate, self).form_valid(form)
        Membership.objects.create(user=self.request.user, group=self.object,
                                  color="{:06x}".format(random.randint(0, 0xFFFFFF)))
        return response


class GroupNameChange(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupFormName
    template_name = 'notes/group_name_change.html'
    success_url = reverse_lazy('group-management')

    def get_object(self, queryset=None):
        group = Group.objects.get(id=self.kwargs['group_id'])
        return group


class GroupColorChange(LoginRequiredMixin, UpdateView):
    model = Membership
    form_class = ColorForm
    template_name = 'notes/group_color_change.html'
    success_url = reverse_lazy('group-management')

    def get_object(self, queryset=None):
        group = Group.objects.get(id=self.kwargs['group_id'])
        membership = Membership.objects.get(group=group, user=self.request.user)

        return membership

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = Group.objects.get(id=self.kwargs['group_id'])
        return context


class GroupPassChange(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupFormPass
    template_name = 'notes/group_pass_change.html'
    success_url = reverse_lazy('group-management')

    def get_object(self, queryset=None):
        group = Group.objects.get(id=self.kwargs['group_id'])
        return group


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
