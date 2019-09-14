from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.db.models import Q
from music.models import Music
from .forms import CreateMusicForm


class CreateMusicView(CreateView):
    template_name = 'createmusic/create_music.html'
    form_class = CreateMusicForm
    success_url = reverse_lazy('create_music:working_music_list')

    def get_form_kwargs(self):
        kwargs = super(CreateMusicView, self).get_form_kwargs()
        kwargs['music_owner'] = self.request.user
        return kwargs


class WorkingMusicListView(ListView):
    template_name = 'createmusic/working_music_list.html'
    model = Music
    context_object_name = 'working_music_list'

    def get_queryset(self):
        queryset = self.model.objects.filter(Q(music_option=Music.MUSIC_NOT_COMPLETED))
        return queryset


class WorkingMusicDetailView(DetailView):
    template_name = 'createmusic/working_music_detail.html'
    model = Music
    pk_url_kwarg = 'working_music_id'

    def get_context_data(self, **kwargs):
        context = super(WorkingMusicDetailView, self).get_context_data(**kwargs)
        context['working_music'] = self.object
        return context
