"""StackOfMusic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import HomeView, CompletedMusicRetrieveView, CompletedMusicDetailTemplateView, LikeMusicAPIView, \
    LikeMusicUpdateAPI
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('<int:completed_music_id>/', CompletedMusicDetailTemplateView.as_view(), name='completed_music_detail'),
    path('RetrieveAPI/<int:completed_music_id>/', CompletedMusicRetrieveView.as_view(), name='completed_music_detail_api'),
    path('LikeMusicAPI/<int:completed_music_id>', LikeMusicAPIView.as_view(), name='like_music_api'),
    path('LikeMusicUpdateAPI/<int:pk>', LikeMusicUpdateAPI, name='like_music_update'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('create/', include('createmusic.urls', namespace='create_music')),
    path('instrument/search/', include('instrument.urls', namespace='instrument_search')),
    path('s3direct/', include('s3direct.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
