from django.urls import path
from .views import CreateMusicView, WorkingMusicDetailView, WorkingMusicListView

app_name = 'create_music'

urlpatterns = [
    path('', CreateMusicView.as_view(), name='create_music'),
    path('list/', WorkingMusicListView.as_view(), name='working_music_list'),
    path('list/<int:working_music_id>', WorkingMusicDetailView, name='working_music_detail'),
]