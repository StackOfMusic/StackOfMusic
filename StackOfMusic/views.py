from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from rest_framework import mixins, generics

from music.models import Music
from .serializer import CompletedMusicSerializer


class HomeView(ListView):
    template_name = 'StackOfMusic/home.html'
    model = Music
    context_object_name = 'completed_music_list'

    def get_queryset(self):
        queryset = self.model.objects.filter(music_option=Music.MUSIC_COMPLETED).order_by('-create_date')[:5]
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data(object_list=None, **kwargs)
        context['hot_list'] = Music.objects.order_by('like')[:5]
        return context


class CompletedMusicDetailView(DetailView):
    template_name = 'StackOfMusic/music_detail.html'
    model = Music
    pk_url_kwarg = 'completed_music_id'

    def get_queryset(self):
        queryset = super(CompletedMusicDetailView, self).get_queryset()
        completed_music_id = self.kwargs.get('completed_music_id')
        return queryset.filter(id=completed_music_id)

    def get_context_data(self, **kwargs):
        context = super(CompletedMusicDetailView, self).get_context_data(**kwargs)
        context['completed_music'] = Music.objects.filter(pk=self.kwargs.get('completed_music_id'))
        return context

    def render_to_response(self, context, **response_kwargs):
        super(CompletedMusicDetailView, self).render_to_response(context, **response_kwargs)
        return JsonResponse(context, **response_kwargs)


class CompletedMusicRetrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    lookup_url_kwarg = 'completed_music_id'
    serializer_class = CompletedMusicSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        super(CompletedMusicRetrieveView, self).setup(request, *args, **kwargs)
        self.completed_music_id = self.kwargs.get('completed_music_id')

    def get_queryset(self):
        queryset = Music.objects.all()
        return queryset


class CompletedMusicDetailTemplateView(TemplateView):
    template_name = 'StackOfMusic/music_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CompletedMusicDetailTemplateView, self).get_context_data(**kwargs)
        context['completed_music_id'] = self.kwargs.get('completed_music_id')

        return context
