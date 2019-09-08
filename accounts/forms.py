from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'sex',
            'age',
        )


class LoginForm(AuthenticationForm):
    error_messages = '비밀번호가 틀렸습니다.'
