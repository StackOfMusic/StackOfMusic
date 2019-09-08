from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import CreateUserForm, LoginForm


class CreateUserView(CreateView):
    template_name = 'accounts/create_user.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('accounts:accounts_create_done')


class CreateUserDoneView(TemplateView):
    template_name = 'accounts/create_user_done.html'


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get_success_url(self):
        url = super(UserLoginView, self).get_success_url()
        url = reverse_lazy('home')
        return url

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


class UserLogoutView(RedirectView):

    def get(self, request, *args, **kwargs):
        url = super(UserLogoutView, self).get_redirect_url(*args, **kwargs)
        auth_logout(request)
        return url
