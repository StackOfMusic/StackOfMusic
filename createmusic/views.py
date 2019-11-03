from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, DeleteView, TemplateView, UpdateView
from rest_framework import mixins, generics

from music.models import Music, SubMusic
from .forms import CreateMusicForm, CreateSubMusicForm
from .serializer import WorkingMusicRetrieveSerializer, SubMusicSerializer

login_url = reverse_lazy('accounts:accounts_login')


class CreateMusicView(CreateView):
    template_name = 'createmusic/create_music.html'
    form_class = CreateMusicForm
    success_url = reverse_lazy('create_music:working_music_list')

    def get_form_kwargs(self):
        kwargs = super(CreateMusicView, self).get_form_kwargs()
        kwargs['music_owner'] = self.request.user
        return kwargs

    @method_decorator(login_required(login_url=login_url))
    def post(self, request, *args, **kwargs):
        return super(CreateMusicView, self).post(request, *args, **kwargs)


class WorkingMusicListView(ListView):
    template_name = 'createmusic/working_music_list.html'
    model = Music
    context_object_name = 'working_music_list'

    def get_queryset(self):
        queryset = self.model.objects.filter(music_option=Music.MUSIC_NOT_COMPLETED).order_by('-create_date')[:5]
        # queryset = self.request.user.music_owner.filter(Q(music_option=Music.MUSIC_NOT_COMPLETED))
        return queryset

    @method_decorator(login_required(login_url=login_url))
    def get(self, request, *args, **kwargs):
        return super(WorkingMusicListView, self).get(request, *args, **kwargs)


class WorkingMusicDetailView(DetailView):
    template_name = 'createmusic/working_music_detail.html'
    model = Music
    pk_url_kwarg = 'working_music_id'

    def get_context_data(self, **kwargs):
        context = super(WorkingMusicDetailView, self).get_context_data(**kwargs)
        context['working_music'] = self.object
        return context


class WorkingMusicRetrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = Music.objects.all()
    lookup_url_kwarg = 'working_music_id'
    serializer_class = WorkingMusicRetrieveSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        super(WorkingMusicRetrieveView, self).setup(request, *args, **kwargs)
        self.woking_music_id = self.kwargs.get('working_music_id')


class WorkingMusicRetrieveTemplateView(TemplateView):
    template_name = 'createmusic/working_music_detail.html'
    pk_url_kwarg = 'working_music_id'

    def get_context_data(self, **kwargs):
        context = super(WorkingMusicRetrieveTemplateView, self).get_context_data(**kwargs)
        context['working_music_id'] = self.kwargs.get('working_music_id')
        return context


class WorkingMusicDeleteView(DeleteView):
    template_name = 'createmusic/working_music_delete.html'
    model = Music
    pk_url_kwarg = 'working_music_id'
    success_url = reverse_lazy('create_music:working_music_list')


class SubMusicCreateView(CreateView):
    template_name = 'createmusic/create_submusic.html'
    form_class = CreateSubMusicForm
    pk_url_kwarg = 'working_music_id'

    def get_form_kwargs(self):
        kwargs = super(SubMusicCreateView, self).get_form_kwargs()
        kwargs['working_music_id'] = self.kwargs.get('working_music_id')
        kwargs['music_contributor'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SubMusicCreateView, self).get_context_data(**kwargs)
        context['working_music_id'] = self.kwargs.get('working_music_id')
        return context

    def get_success_url(self):
        working_music_id = self.kwargs.get('working_music_id')
        return reverse_lazy('create_music:working_music_detail', kwargs={'working_music_id': working_music_id})

    def post(self, request, *args, **kwargs):
        return super(SubMusicCreateView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SubMusicCreateView, self).get(request, *args, **kwargs)


class MusicUpdateView(UpdateView):

    queryset = Music.objects.all()
    lookup_url_kwarg = 'working_music_id'
    serializer_class = WorkingMusicRetrieveSerializer

    def post(self, request, *args, **kwargs):
        return super(MusicUpdateView, self).post(request, *args, **kwargs)
