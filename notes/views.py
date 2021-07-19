from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import SNote, SComment, CustomUser, NoteGroup
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login
from .forms import SignUpForm
from django.http import HttpResponse


class CustomLoginView(LoginView):
    template_name = 'notes/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    success_url = reverse_lazy('notes')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('notes')


class UserRegistration(FormView):
    template_name = 'notes/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        user = form.save()
        # if user is not None:
        #    login(self, user)
        return super(UserRegistration, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('notes')
        return super(UserRegistration, self).get(*args, **kwargs)


class MyNotesList(LoginRequiredMixin, ListView):
    model = SNote
    context_object_name = 'notes_list'
    template_name = "notes/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes_list'] = SNote.objects.filter((Q(to_whom=self.request.user)
                                                      | Q(to_whom=None, author=self.request.user))
                                                     & Q(is_for_group=False))
        return context


class GroupNotesList(LoginRequiredMixin, ListView):
    model = SNote
    context_object_name = 'notes_list'
    template_name = "notes/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authors = CustomUser.objects.filter(Q(note_group=self.request.user.note_group)
                                            & ~Q(note_group=None))
        context['notes_list'] = SNote.objects.filter(Q(is_for_group=True) & Q(author__in=authors))
        return context


class NoteAdd(LoginRequiredMixin, CreateView):
    model = SNote
    template_name = 'notes/add.html'
    fields = ['heading', 'message', 'to_whom', 'is_for_group']
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NoteAdd, self).form_valid(form)

    def get_form_class(self):
        print(self.request.user.note_group)
        if self.request.user.note_group is None:
            self.fields = ['heading', 'message']
        else:
            self.fields = self.fields
        return super(NoteAdd, self).get_form_class()


class NoteUpdate(LoginRequiredMixin, UpdateView):
    model = SNote
    fields = ['heading', 'message', 'to_whom', 'is_for_group']
    success_url = reverse_lazy('notes')

    def get_form_class(self):
        print(self.request.user.note_group)
        if self.request.user.note_group is None:
            self.fields = ['heading', 'message']
        else:
            self.fields = self.fields
        return super(NoteUpdate, self).get_form_class()


class NoteDelete(LoginRequiredMixin, DeleteView):
    model = SNote
    context_object_name = 'note'
    success_url = reverse_lazy('notes')


class NoteGroupMembers(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'group_members'
    template_name = "notes/group_members.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_members = CustomUser.objects.filter(Q(note_group=self.request.user.note_group))
        context['group_members'] = group_members
        return context


@login_required
def group_member_delete(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if user.group_admin:
        members = CustomUser.objects.filter(Q(note_group=user.note_group) &
                                            Q(group_admin=False))
        new_admin = members[0]
        new_admin.group_admin = True
        new_admin.save()
        user.group_admin = False

    user.note_group = None
    user.save()

    return redirect('home')


class NoteGroupDelete(LoginRequiredMixin, DeleteView):
    model = NoteGroup
    context_object_name = 'group'
    success_url = reverse_lazy('home')

    #add disable group for members logic