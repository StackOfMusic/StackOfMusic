from django.urls import path
from .views import CreateUserView, CreateUserDoneView, UserLoginView, UserLogoutView, UserDetailView, CopyrightTemplateView, UserWorkingProjects

app_name = 'accounts'


urlpatterns = [
    path('create/', CreateUserView.as_view(), name='accounts_create'),
    path('create/done', CreateUserDoneView.as_view(), name='accounts_create_done'),
    path('signin/', UserLoginView.as_view(), name='accounts_login'),
    path('signout/', UserLogoutView.as_view(url='http://localhost:8000'), name='accounts_logout'),
    path('mypage/<int:account_id>', UserDetailView.as_view(), name='accounts_detail'),
    path('mypage/<int:account_id>/copyright/', CopyrightTemplateView.as_view(), name='accounts_copyright'),
    path('mypage/<int:account_id>/myworkingmusic/', UserWorkingProjects.as_view(), name='accounts_working_projects'),
]