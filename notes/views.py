from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import SNote, NoteGroup
from basic.models import CustomUser
from django.db.models import Q

from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import MembersNoteForm, GroupCreationForm


class MyNotesList(LoginRequiredMixin, ListView):
    model = SNote
    context_object_name = 'notes_list'
    template_name = "notes/my_notes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notes_list = SNote.objects.filter((Q(to_whom=self.request.user) | Q(to_whom=None, author=self.request.user))
                                          & Q(is_for_group=False))
        context['notes_list'] = notes_list
        return context


class NoteCreate(LoginRequiredMixin, CreateView):
    template_name = 'notes/note_create.html'
    success_url = reverse_lazy('my-notes')
    form_class = MembersNoteForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NoteCreate, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(NoteCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class NoteUpdate(LoginRequiredMixin, UpdateView):
    model = SNote
    fields = ['heading', 'message', 'to_whom', 'is_for_group']
    success_url = reverse_lazy('my-notes')

    def get_form_class(self):
        if self.request.user.note_group is None:
            self.fields = ['heading', 'message']
        return super(NoteUpdate, self).get_form_class()


class NoteDelete(LoginRequiredMixin, DeleteView):
    model = SNote
    context_object_name = 'note'
    success_url = reverse_lazy('my-notes')


class NoteGroupMembersList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        group = self.request.user.note_group
        if group is None:
            return redirect('home')
        group_members = CustomUser.objects.filter(Q(note_group=group))
        context = {'group': group, 'group_members': group_members}
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
        return redirect('home')
    user.note_group = None
    user.save()
    return redirect('group-members')


class NoteGroupDelete(LoginRequiredMixin, DeleteView):
    model = NoteGroup
    context_object_name = 'group'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        members = CustomUser.objects.filter(note_group=self.request.user.note_group)
        group_notes = SNote.objects.filter(Q(is_for_group=True) & Q(author__in=members))
        for note in group_notes:
            note.delete()
        for member in members:
            member.note_group = None
            member.group_admin = False
            member.save()

        return super(NoteGroupDelete, self).delete(request, *args, **kwargs)


class GroupNotesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.note_group:
            authors = CustomUser.objects.filter(Q(note_group=request.user.note_group) & ~Q(note_group=None))
            group_notes = SNote.objects.filter(Q(is_for_group=True) & Q(author__in=authors))
            context['notes_list'] = group_notes
        return render(request, 'notes/group_notes.html', context)

    def post(self, request, *args, **kwargs):
        group = NoteGroup.objects.filter(id=request.POST['group_id'])
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
        return render(request, 'notes/group_notes.html', context=context)


class NoteGroupCreate(LoginRequiredMixin, CreateView):
    form_class = GroupCreationForm
    template_name = 'notes/group_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = self.request.user
        user.note_group = form.save()
        user.group_admin = True
        user.save()
        return super(NoteGroupCreate, self).form_valid(form)


def kostyl(request):
    return redirect('welcome-page')