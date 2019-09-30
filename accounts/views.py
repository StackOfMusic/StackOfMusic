from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, RedirectView, DetailView
from rest_framework import mixins, generics

from accounts.models import Copyright
from .forms import CreateUserForm, UserAuthenticationForm
from .models import User
from .serializer import CopyrightSerializer


class CreateUserView(CreateView):
    template_name = 'accounts/create_user.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('accounts:accounts_create_done')


class CreateUserDoneView(TemplateView):
    template_name = 'accounts/create_user_done.html'


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = UserAuthenticationForm

    def get_success_url(self):
        super(UserLoginView, self).get_success_url()
        url = reverse_lazy('home')
        return url

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


class UserLogoutView(RedirectView):

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(UserLogoutView, self).get(request, *args, **kwargs)


class UserDetailView(DetailView):
    template_name = 'accounts/mypage.html'
    model = User
    pk_url_kwarg = 'account_id'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['user_music_list'] = self.request.user.music_owner.all()
        return context


class CopyrightAPIView(mixins.ListModelMixin, generics.GenericAPIView):
    object = Copyright.objects.all()
    serializer_class = CopyrightSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CopyrightTemplateView(TemplateView):
    template_name = 'accounts/copyright.html'

    def get_context_data(self, **kwargs):
        context = super(CopyrightTemplateView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
