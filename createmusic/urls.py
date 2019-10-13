from django.urls import path
from .views import CreateMusicView, WorkingMusicDetailView, WorkingMusicListView, WorkingMusicDeleteView, WorkingMusicRetrieveView, WorkingMusicRetrieveTemplateView

app_name = 'create_music'

urlpatterns = [
    path('', CreateMusicView.as_view(), name='create_music'),
    path('list/', WorkingMusicListView.as_view(), name='working_music_list'),
    path('list/<int:working_music_id>/delete/', WorkingMusicDeleteView.as_view(), name='working_music_delete'),
    path('list/<int:working_music_id>/', WorkingMusicRetrieveTemplateView.as_view(), name='working_music_detail'),
    path('list/WorkingMusicRetrieveAPI/<int:working_music_id>/', WorkingMusicRetrieveView.as_view(), name='working_music_detail_api'),
]