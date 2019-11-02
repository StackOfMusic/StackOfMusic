from django.urls import path
from .views import MusicListView, InstrumentSearchResultListAPIView


app_name = 'instrument_search'

urlpatterns = [
    path('', MusicListView.as_view(), name='instrument_search'),
    path('api/<int:instrument_id>', InstrumentSearchResultListAPIView.as_view(), name='instrument_search_api'),
]
