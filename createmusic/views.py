import os

import boto3
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DeleteView, \
    TemplateView, UpdateView, View, DetailView
from pydub import AudioSegment
from rest_framework import mixins, generics

from StackOfMusic import settings
from music.models import Music, SubMusic
from reconstruct_drum.detect_beat import detect_beat
from reconstruct_piano.detect_frequency.detect_freq import detect_freq
from reconstruct_piano.detect_frequency.edit_music import s3_file_download, convert_s3_file_download
from reconstruct_piano.m4a2wav.convert import m4a2wave
from .forms import CreateMusicForm, CreateSubMusicForm
from .serializer import WorkingMusicRetrieveSerializer

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
        return queryset

    @method_decorator(login_required(login_url=login_url))
    def get(self, request, *args, **kwargs):
        return super(WorkingMusicListView, self).get(request, *args, **kwargs)


class WorkingMusicRetrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = Music.objects.all()
    lookup_url_kwarg = 'working_music_id'
    serializer_class = WorkingMusicRetrieveSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class WorkingMusicRetrieveTemplateView(TemplateView):
    template_name = 'createmusic/working_music_detail.html'
    pk_url_kwarg = 'working_music_id'

    def get(self, request, *args, **kwargs):
        return super(WorkingMusicRetrieveTemplateView, self).get(request, *args, *kwargs)

    def get_context_data(self, **kwargs):
        working_music_id = self.kwargs.get(self.pk_url_kwarg)
        context = super(WorkingMusicRetrieveTemplateView, self).get_context_data(**kwargs)
        context['working_music_id'] = working_music_id
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


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


class LoopStationView(DetailView):
    template_name = 'createmusic/loopstation.html'
    pk_url_kwarg = 'working_music_id'

    def get_queryset(self):
        working_music_id = self.kwargs.get(self.pk_url_kwarg)
        queryset = Music.objects.filter(pk=working_music_id)
        return queryset

    def get_context_data(self, **kwargs):
        working_music_id = self.kwargs.get(self.pk_url_kwarg)
        context = super(LoopStationView, self).get_context_data(**kwargs)
        context['sub_musics'] = Music.objects.get(pk=working_music_id).sub_musics.all()
        return context


class SubMusicMergeView(View):

    pk_url_kwarg = 'working_music_id'

    def post(self, request, *args, **kwargs):
        submusic_pk = request.POST.get('data')
        music_pk = self.kwargs.get(self.pk_url_kwarg)
        if Music.objects.get(id=music_pk).owner != self.request.user:
            message = '권한이 없습니다.'
            return JsonResponse(status=403, data={'message': message})

        submusic = get_object_or_404(SubMusic, pk=submusic_pk)
        submusic.status = 0
        submusic.save()
        message = '성공!'
        return JsonResponse(status=200, data={'message': message})

    def get(self, request, *args, **kwrags):
        message = '잘못된 접근입니다'
        return JsonResponse(status=405, data={'message': message})


class SubMusicDeleteView(View):

    pk_url_kwargs = 'working_music_id'

    def post(self, request, *args, **kwargs):
        submusic_pk = request.POST.get('data')
        music_pk = self.kwargs.get(self.pk_url_kwargs)

        if  Music.objects.get(id=music_pk).owner != self.request.user:
            message = '권한이 없습니다.'
            return JsonResponse(status=403, data={'message': message})

        sub_music = get_object_or_404(SubMusic, pk=submusic_pk)
        sub_music.delete()

        message = '삭제가 완료되었습니다.'
        return JsonResponse(status=200, data={'message': message})

    def get(self, request, *args, **kwargs):
        message = '잘못된 접근입니다.'
        return JsonResponse(status=403, data={'message': message})


class MusicStatusChangeView(UpdateView):
    model = Music
    pk_url_kwarg = 'working_music_id'
    fields = [
        'music_option'
    ]

    def post(self, request, *args, **kwargs):
        working_music_id = self.kwargs.get('working_music_id')
        if Music.objects.get(id=working_music_id).owner == self.request.user:
            return super(MusicStatusChangeView, self).post(request, *args, **kwargs)
        raise Http404

    def get(self, request, *args, **kwargs):
        raise Http404

    def get_success_url(self):
        working_music_id = self.kwargs.get('working_music_id')
        return reverse_lazy('create_music:working_music_detail', kwargs={'working_music_id': working_music_id})

    def form_invalid(self, form):
        return super(MusicStatusChangeView, self).form_valid(form)

    def form_valid(self, form):
        working_music_id = self.kwargs.get('working_music_id')
        Music.objects.get(id=working_music_id).music_option = int(form.data['music_option'])
        self.object = form.save()
        return HttpResponseRedirect(reverse_lazy('create_music:working_music_list'))


class VoiceToPianoView(View):

    def post(self,  request, *args, **kwargs):
        pk = request.POST.get('data')
        if SubMusic.objects.get(id=pk).contributor == request.user:
            submusic = get_object_or_404(SubMusic, pk=pk)
            submusic.update_status = 1
            submusic.save()
            detect_freq(pk)
            message = '변환중 입니다.'
            return JsonResponse(status=200, data={'message': message})
        message = '권한이 없습니다.'
        return JsonResponse(status=403, data={'message': message})

    def get(self, request, *args, **kwargs):
        message = "잘못된 접근입니다."
        return JsonResponse(status=403, data={'message': message})


class VoiceToDrumView(View):

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('data')
        if SubMusic.objects.get(id=pk).contributor == request.user:
            submusic=get_object_or_404(SubMusic, pk=pk)
            submusic.update_status = 1
            submusic.save()
            detect_beat(pk)
            return JsonResponse(status=200, data={'message': pk})
        message = '권한이 없습니다.'
        return JsonResponse(status=403, data={'message': message})

    def get(self, request, *args, **kwargs):
        message = "잘못된 접근입니다."
        return JsonResponse(status=403, data={'message': message})


class MusicConvertCheckView(View):

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('data')
        status = get_object_or_404(SubMusic, pk=pk).update_status
        if status == 1:
            return JsonResponse(status=200, data={'message': status})
        elif status == 2:
            message = '변환이 완료되었습니다.'
            return JsonResponse(status=200, data={'message': status})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class MusicCompletedView(View):
    pk_url_kwarg = 'working_music_id'

    def post(self, request, *args, **kwargs):
        submusic_name_list = []
        file_path = settings.BASE_DIR
        working_music_id = self.kwargs.get(self.pk_url_kwarg)
        music_object = get_object_or_404(Music, pk=working_music_id)
        if music_object.owner == request.user:
            media_file_location = settings.STATICFILES_LOCATION

            music_name = get_object_or_404(Music, pk=working_music_id).seed_file.name
            url = 'https://' + settings.AWS_S3_CUSTOM_DOMAIN + '/' + media_file_location + '/' + music_name
            music_name = music_name.replace('audiofile/', '')
            submusic_name_list.append(music_name)
            request = requests.get(url, stream=True)
            if request.status_code == 200:
                with open(music_name, 'wb') as f:
                    for chunk in request.iter_content(1024):
                        f.write(chunk)

            for i in range(music_object.sub_musics.values_list().__len__()):
                if music_object.sub_musics.values_list()[i][8] == 2:
                    convert_s3_file_download(music_object.sub_musics.values_list()[i][0])
                    convert_name = music_object.sub_musics.values_list()[i][5]
                    if 'audiofile/' in convert_name:
                        convert_name = music_object.sub_musics.values_list()[i][5].replace('audiofile/', '')
                    submusic_name_list.append(convert_name)
                elif music_object.sub_musics.values_list()[i][8] == 0:
                    s3_file_download(music_object.sub_musics.values_list()[i][0])
                    submusic_name_list.append(music_object.sub_musics.values_list()[i][4][10:])

        self.combine_music(file_path, submusic_name_list)

        return HttpResponseRedirect(reverse_lazy('home'))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def combine_music(self, path, file_list):
        song_list = []
        count = 0
        for filename in file_list:
            fullpath = os.path.join(path, filename)
            ext = os.path.splitext(filename)
            if ext[1] != '.wav':
                m4a2wave(filename)
                filename = ext[0] + '.wav'
                fullpath = os.path.join(path, filename)
                file_list[count] = filename
            count = count + 1
            song_list.append(AudioSegment.from_wav(fullpath))

        combined_song = song_list[0]
        for i in range(1, len(song_list)):
            combined_song.overlay(song_list[i])

        result_name = settings.BASE_DIR + "/combined_" + file_list[0]

        combined_song.export(result_name, format='wav')
        self.combine_music_save('combined_' + file_list[0])

        for filename in file_list:
            fullpath = os.path.join(path, filename)
            os.remove(fullpath)

    def combine_music_save(self, complete_file_name):
        complete_file_path = settings.BASE_DIR + '/' + complete_file_name
        working_music_id = self.kwargs.get(self.pk_url_kwarg)
        with open(complete_file_path, 'rb') as f:
            contents = f.read()

        complete_music = get_object_or_404(Music, pk=working_music_id)
        complete_music.music_option = 0
        complete_music.completed_music.name = 'new_' + complete_file_name
        s3 = boto3.resource(
            's3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        bucket = s3.Bucket('stackofmusic')
        bucket.put_object(Key=complete_music.completed_music.name, Body=contents)

        complete_music.save()
        os.remove(complete_file_path)
