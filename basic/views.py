from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm
from django.contrib.auth import login


def main(request):
    if request.user.is_authenticated:
        return redirect('my-notes')
    return render(request, 'basic/main.html')


class UserRegistration(FormView):
    template_name = 'basic/user_registration.html'
    form_class = SignUpForm
    success_url = reverse_lazy('my-notes')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegistration, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('my-notes')
        return super(UserRegistration, self).get(*args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'basic/user_login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    success_url = reverse_lazy('my-notes')

    def get_success_url(self):
        return reverse_lazy('my-notes')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('start-page')
