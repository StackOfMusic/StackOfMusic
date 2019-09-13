from django.urls import path
from .views import CreateMusicView, WorkingMusicDetailView

app_name = 'create_music'

urlpatterns = [
    path('', CreateMusicView.as_view(), name='create_music'),
    path('<int:working_music_id>', WorkingMusicDetailView, name='working_music_detail'),
]