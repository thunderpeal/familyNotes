from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import SNote, SComment, CustomUser
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.db.models import Q

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
        #if user is not None:
        #    login(self, user)
        return super(UserRegistration, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('notes')
        return super(UserRegistration, self).get(*args, **kwargs)


class NotesList(LoginRequiredMixin, ListView):
    model = SNote
    context_object_name = 'notes_list'
    template_name = "notes/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes_list'] = SNote.objects.filter(Q(to_whom=self.request.user)
                                                     | Q(to_whom=None, author=self.request.user))
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
