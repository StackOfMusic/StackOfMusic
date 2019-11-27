import os

import boto
import wget
from celery import Celery
from pydub import AudioSegment

from StackOfMusic import settings
from music.models import SubMusic
from reconstruct_piano.m4a2wav.convert import m4a2wave

from django.shortcuts import get_object_or_404

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StackOfMusic.settings')
app = Celery('StackOfMusic')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIANO_PATH = os.path.join(BASE_DIR, 'detect_frequency/')
PIANO_RAW_PATH = os.path.join(PIANO_PATH, 'piano-raw/')
MUSIC_ELEMENT_PATH = os.path.join(PIANO_PATH, 'music_element/')
MUSIC_SOURCE_PATH = os.path.join(PIANO_PATH, 'audiofile/')


def s3_file_download(pk):
    connect = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    media_file_location = settings.STATICFILES_LOCATION

    music_name = get_object_or_404(SubMusic, pk=pk).music_file.name
    url = 'https://' + settings.AWS_S3_CUSTOM_DOMAIN + '/' + media_file_location + '/' + music_name
    wget.download(url, MUSIC_SOURCE_PATH)


def divide_music(pk):

    music_name = get_object_or_404(SubMusic, pk=pk).music_file.name

    music_name = music_name[10:]
    m4a2wave(music_name)
    music_name = os.path.splitext(music_name)[0]
    music_name = music_name + '.wav'

    song = AudioSegment.from_wav(MUSIC_SOURCE_PATH + '/' + music_name)

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
