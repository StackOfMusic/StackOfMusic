from django.views.generic import ListView, TemplateView, DetailView
from music.models import Music


class HomeView(ListView):
    template_name = 'home.html'
    model = Music
    context_object_name = 'music_list'

    def get_queryset(self):
        queryset = Music.objects.filter(music_option=self.model.MUSIC_COMPLETED).order_by('-create_date')[:5]
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data(object_list=None, **kwargs)
        context['hot_list'] = Music.objects.order_by('like')[:5]
        return context


class MusicDetailView(DetailView):
    template_name = 'music_detail.html'
    model = Music
    pk_url_kwarg = 'music_id'

    def get_context_data(self, **kwargs):
        context = super(MusicDetailView, self).get_context_data(**kwargs)
        context['music_list'] = self.object.all
        return context
