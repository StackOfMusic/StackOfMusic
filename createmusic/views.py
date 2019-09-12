from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from .forms import CreateMusicForm
from music.models import Music


class CreateMusicView(CreateView):
    template_name = ''
    form_class = CreateMusicForm
    success_url = reverse_lazy('')

    def get_form_kwargs(self):
        kwargs = super(CreateMusicView, self)
        kwargs['user'] = self.request.user
        return kwargs


class WorkingMusicListView(ListView):
    template_name = 'createmusic/working_music_list'
    model = Music

    def get_queryset(self):
        pass


class CreateMusicDetailView(DetailView):
    template_name = ''
    model = Music
    pk_url_kwarg = 'create_music_id'
