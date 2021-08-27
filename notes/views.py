from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import SNote, Group
from basic.models import CustomUser
from django.db.models import Q

from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import NoteForm, GroupCreationForm


class NotesLists(LoginRequiredMixin, ListView):
    model = SNote
    template_name = "notes/notes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = self.request.user.members_groups.all()
        if groups:
            context['groups_available'] = True
            group_notes = dict()
            for group in groups:
                notes_per_g = SNote.objects.filter(Q(group=group))
                group_notes[group] = notes_per_g

            context['group_notes_list'] = group_notes

        my_notes_list = SNote.objects.filter((Q(to_whom=self.request.user) | Q(to_whom=None, author=self.request.user))
                                          & Q(group=None))
        context['my_notes_list'] = my_notes_list
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


class NoteUpdate(LoginRequiredMixin, UpdateView):
    model = SNote
    fields = ['heading', 'message', 'group', 'to_whom']
    success_url = reverse_lazy('notes')

    def get_form_class(self):
        if not self.request.user.members_groups.all():
            self.fields = ['heading', 'message']
        return super(NoteUpdate, self).get_form_class()


class NoteDelete(LoginRequiredMixin, DeleteView):
    model = SNote
    context_object_name = 'note'
    success_url = reverse_lazy('notes')


class GroupMembersList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        groups = self.request.user.members_groups.all()
        if not groups:
            return redirect('notes')
        groups_members = {}
        for group in groups:
            groups_members['group'] = group.members.all()
        context = {'groups': groups, 'groups_members': groups_members}
        return render(request, 'notes/group_members.html', context=context)


@login_required
def group_member_delete(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if user.group_admin:
        members = CustomUser.objects.filter(Q(note_group=user.note_group) & Q(group_admin=False))
        if members:
            new_admin = members[0]
            new_admin.group_admin = True
            new_admin.save()
            user.note_group = None
        else:
            group = user.note_group
            user.note_group = None
            user.save()
            group.delete()
        user.group_admin = False
        user.save()
        return redirect('group-login')
    user.note_group = None
    user.save()
    return redirect('group-members')


class GroupDelete(LoginRequiredMixin, DeleteView):
    model = Group
    context_object_name = 'group'
    success_url = reverse_lazy('group-login')

    def delete(self, request, *args, **kwargs):
        members = CustomUser.objects.filter(note_group=self.request.user.note_group)
        group_notes = SNote.objects.filter(Q(is_for_group=True) & Q(author__in=members))
        for note in group_notes:
            note.delete()
        for member in members:
            member.note_group = None
            member.group_admin = False
            member.save()

        return super(GroupDelete, self).delete(request, *args, **kwargs)


class GroupLoginView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.members_groups.all():
            redirect('group-members')
        return render(request, 'notes/group_login.html')

    def post(self, request, *args, **kwargs):
        group = Group.objects.filter(id=request.POST['group_id'])
        if group:
            if group[0].password == request.POST['password']:
                user = request.user
                user.note_group = group[0]
                user.save()
                return redirect('group-members')
            failure = 'Wrong password.'
        else:
            failure = 'There is no group with given id.'

        context = {'failure': failure, 'searched_id': request.POST['group_id']}
        return render(request, 'notes/group_members.html', context=context)


class GroupCreate(LoginRequiredMixin, CreateView):
    form_class = GroupCreationForm
    template_name = 'notes/group_registration.html'
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        form.instance.admin = self.request.user
        response = super(GroupCreate, self).form_valid(form)
        self.object.members.add(self.request.user)
        return response


class CustomTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'notes/settings.html'


def kostyl(request):
    return redirect('welcome-page')

