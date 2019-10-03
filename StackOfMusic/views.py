from django.views.generic import ListView, DetailView

from music.models import Music


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

    def get_context_data(self, **kwargs):
        context = super(CompletedMusicDetailView, self).get_context_data(**kwargs)
        context['completed_music'] = self.object
        return context
