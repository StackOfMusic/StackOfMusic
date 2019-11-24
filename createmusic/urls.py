from django.urls import path

from .views import CreateMusicView, WorkingMusicListView, WorkingMusicDeleteView, WorkingMusicRetrieveView, \
    WorkingMusicRetrieveTemplateView, MusicMergeView, SubMusicCreateView, MusicStatusChangeView, SubMusicDeleteView, \
    VoiceToDrumView, VoiceToPianoView, LoopStationView

app_name = 'create_music'



urlpatterns = [
    path('', CreateMusicView.as_view(), name='create_music'),
    path('list/', WorkingMusicListView.as_view(), name='working_music_list'),
    path('list/<int:working_music_id>/delete/', WorkingMusicDeleteView.as_view(), name='working_music_delete'),
    path('list/<int:working_music_id>/', WorkingMusicRetrieveTemplateView.as_view(), name='working_music_detail'),
    path('list/WorkingMusicRetrieveAPI/<int:working_music_id>/', WorkingMusicRetrieveView.as_view(), name='working_music_detail_api'),
    path('list/<int:working_music_id>/SubMusicCreate', SubMusicCreateView.as_view(), name='sub_music_create'),
    path('list/<int:working_music_id>/LoopStaion', LoopStationView.as_view(), name='loopstaion'),
    path('list/<int:working_music_id>/MusicUpdate', MusicMergeView.as_view(), name='music_update'),
    path('list/<int:working_music_id>/SubMusicDelete', SubMusicDeleteView.as_view(), name='submusic_delete'),
    path('list/<int:working_music_id>/MusicStatusUpdate', MusicStatusChangeView.as_view(), name='music_status_change'),
]