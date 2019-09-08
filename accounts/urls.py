from django.urls import path
from .views import CreateUserView, CreateUserDoneView, UserLoginView

app_name = 'accounts'


urlpatterns = [
    path('create/', CreateUserView.as_view(), name='accounts_create'),
    path('create/done', CreateUserDoneView.as_view(), name='accounts_create_done'),
    path('signin/', UserLoginView.as_view(), name='accounts_login'),
]