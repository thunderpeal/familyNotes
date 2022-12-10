from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm, CustomAuthForm, AccountSettings
from django.contrib.auth import login
from .models import CustomUser
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from notes.models import Notification


def welcome_page(request):
    if request.user.is_authenticated:
        return redirect('notes')
    return render(request, 'basic/welcome_page.html')


class UserSignUp(FormView):
    template_name = 'basic/user_signUp.html'
    form_class = SignUpForm
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserSignUp, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('notes')
        return super(UserSignUp, self).get(*args, **kwargs)


class CustomSignInView(LoginView):
    template_name = 'basic/user_signIn.html'
    form_class = CustomAuthForm
    fields = '__all__'
    redirect_authenticated_user = True
    success_url = reverse_lazy('notes')

    def get_success_url(self):
        return reverse_lazy('notes')


class CustomSignOutView(LogoutView):
    next_page = reverse_lazy('welcome-page')


class CustomTemplateView(LoginRequiredMixin, TemplateView):
    """
    This view is used to display static page that contains information for users to read. Like what is this site,
    how to use it adn etc
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications_length = Notification.objects.filter((Q(user=self.request.user) & Q(is_read=False))).count()
        context['notifications_length'] = notifications_length
        return context

    template_name = 'basic/settings.html'


class PersonProfileView(LoginRequiredMixin, UpdateView):
    form_class = AccountSettings
    model = CustomUser
    template_name = 'basic/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications_length = Notification.objects.filter((Q(user=self.request.user) & Q(is_read=False))).count()
        context['notifications_length'] = notifications_length
        return context

    def get_success_url(self):
        return reverse('profile', args=(self.request.user.id, ))
