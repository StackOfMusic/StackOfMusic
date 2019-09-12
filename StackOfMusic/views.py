from django.views.generic import ListView, TemplateView
from music.models import Music


class HomeView(ListView):
    template_name = 'home.html'
    model = Music

    def get_queryset(self):
        queryset = Music.objects.order_by('-create_date')[:5]
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data(object_list=None, **kwargs)
        context['hot_list'] = Music.objects.order_by('like')[:5]
        return context

