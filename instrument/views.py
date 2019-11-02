from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from rest_framework import mixins, generics
from rest_framework.response import Response

from instrument.forms import MusicSearchForm
from music.models import Music
from .serializer import InstrumentSerializer


class MusicListView(ListView):
    template_name = 'instrument/instrument_list.html'
    context_object_name = 'music_list'
    model = Music

    def get_queryset(self):
        queryset = super(MusicListView, self).get_queryset()
        instrument_id_list = self.request.GET.getlist('instruments')
        search_word = self.request.GET.get('search_word')

        if search_word:
            queryset = queryset.filter(title__contains=search_word)

        if instrument_id_list:
            queryset = queryset.filter(
                instrument_id__in=instrument_id_list,
                sub_musics__instrument_id__in=instrument_id_list,
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MusicListView, self).get_context_data(object_list=None, **kwargs)
        context['form'] = MusicSearchForm(self.request.GET)
        return context


class InstrumentSearchResultListAPIView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Music.objects.all()
    serializer = InstrumentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        data = request.GET.get('data')
        self.queryset = Music.objects.filter(instrument_id=data)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(InstrumentSearchResultListAPIView, self).dispatch(request, *args, **kwargs)
