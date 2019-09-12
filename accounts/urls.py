from django.urls import path
from .views import CreateUserView, CreateUserDoneView, UserLoginView, UserLogoutView, UserDetailView

app_name = 'accounts'


urlpatterns = [
    path('create/', CreateUserView.as_view(), name='accounts_create'),
    path('create/done', CreateUserDoneView.as_view(), name='accounts_create_done'),
    path('signin/', UserLoginView.as_view(), name='accounts_login'),
    path('signout/', UserLogoutView.as_view(url='http://localhost:8000'), name='accounts_logout'),
    path('<int:account_id>', UserDetailView.as_view(), name= 'accounts_detail'),
]