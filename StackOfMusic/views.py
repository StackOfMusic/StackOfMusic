from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, TemplateView
from rest_framework import mixins, generics, permissions
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication

from accounts.models import User
from music.models import Music
from .serializer import CompletedMusicSerializer, LikeMusicSerializer

login_url = reverse_lazy('accounts:accounts_login')


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
        context['user'] = User.objects.all()
        return context


# @method_decorator(login_required(login_url=login_url))
class LikeMusicAPIView(mixins.UpdateModelMixin, generics.GenericAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = LikeMusicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        complete_music_id = request.POST['pk']
        complete_music = get_object_or_404(Music, id=complete_music_id)
        filtered_like_music = self.request.user.liked_music.filter(id=complete_music_id)
        user = self.request.user
        if filtered_like_music.exist():
            user.liked_music.remove(complete_music)
        else:
            user.liked_music.add(complete_music)

        return super(LikeMusicAPIView, self).update(request, *args, **kwargs)


@csrf_exempt
def LikeMusicUpdateAPI(request, pk):
    music = get_object_or_404(Music, pk=pk)
    user = User.objects.get(username=request.user)
    if music.liked_music.filter(id=user.id).exists():
        music.liked_music.remove(user)
    else:
        music.liked_music.add(user)
    context = {'total_music_like': str(music.total_likes_user)}
    return JsonResponse(context, json_dumps_params={'ensure_ascii': True})
