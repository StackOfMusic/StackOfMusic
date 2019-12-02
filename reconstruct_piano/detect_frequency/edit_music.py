import os

import boto
import wget
import requests
from celery import Celery
from django.shortcuts import get_object_or_404
from pydub import AudioSegment

from StackOfMusic import settings
from music.models import SubMusic
from reconstruct_piano.m4a2wav.convert import m4a2wave

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StackOfMusic.settings')
app = Celery('StackOfMusic')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIANO_PATH = os.path.join(BASE_DIR, 'detect_frequency/')
PIANO_RAW_PATH = os.path.join(PIANO_PATH, 'piano-raw/')
MUSIC_ELEMENT_PATH = os.path.join(PIANO_PATH, 'music_element/')
MUSIC_SOURCE_PATH = os.path.join(PIANO_PATH, 'audiofile')


def convert_s3_file_download(pk):
    sub_music_name = get_object_or_404(SubMusic, pk=pk).convert_music_file.name
    url = 'https://' + settings.AWS_S3_CUSTOM_DOMAIN + '/' + sub_music_name
    sub_music_name = sub_music_name.replace('audiofile/', '')
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(sub_music_name, 'wb') as f:
            for chunk in request.iter_content(1024):
                f.write(chunk)


def s3_file_download(pk):
    media_file_location = settings.STATICFILES_LOCATION

    sub_music_name = get_object_or_404(SubMusic, pk=pk).music_file.name

    url = 'https://' + settings.AWS_S3_CUSTOM_DOMAIN + '/' + media_file_location + '/' + sub_music_name
    sub_music_name = sub_music_name.replace('audiofile/', '')
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(sub_music_name, 'wb') as f:
            for chunk in request.iter_content(1024):
                f.write(chunk)


def divide_music(pk):

    s3_file_download(pk)

    music_name = get_object_or_404(SubMusic, pk=pk).music_file.name
    music_name = music_name.replace('audiofile/', '')
    print(music_name)
    ext = os.path.splitext(music_name)[1]
    if ext != '.wav':
        m4a2wave(music_name)
    music_name = os.path.splitext(music_name)[0]
    music_name = music_name + '.wav'

    # song = AudioSegment.from_wav(MUSIC_SOURCE_PATH + '/' + music_name)
    song = AudioSegment.from_wav(settings.BASE_DIR + '/' + music_name)

    start_postion = 2000
    elements = 0 + 2000
    result_index = 0
    song_len = len(song)
    element_size = 400

    while elements < song_len:
        if elements + element_size < song_len:
            music_elements = song[elements:elements + element_size]
        else:
            music_elements = song[elements:song_len]
        elements = elements + element_size

        result_name = MUSIC_ELEMENT_PATH + '{}.wav'.format(result_index)
        result_index = result_index + 1
        music_elements.export(result_name, format='wav')
