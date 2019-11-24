from pydub import AudioSegment
import boto
import wget
from StackOfMusic import settings
from music.models import SubMusic
from celery import Celery
import os
from reconstruct_piano.m4a2wav.convert import m4a2wave
from threading import Thread

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StackOfMusic.settings')
app = Celery('StackOfMusic')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIANO_PATH = os.path.join(BASE_DIR, 'detect_frequency')
PIANO_RAW_PATH = os.path.join(PIANO_PATH, 'piano-raw')
MUSIC_ELEMENT_PATH = os.path.join(PIANO_PATH, 'music_element')
MUSIC_SOURCE_PATH = os.path.join(PIANO_PATH, 'audiofile')


def s3_file_download(pk):
    connect = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    media_file_location = settings.STATICFILES_LOCATION

    music_name = SubMusic.objects.get(id=pk).music.seed_file
    music_name = str(music_name)
    url = 'https://' + settings.AWS_S3_CUSTOM_DOMAIN + '/' + media_file_location + '/' + music_name
    print(MUSIC_SOURCE_PATH)
    filename = wget.download(url, MUSIC_SOURCE_PATH)


def divide_music(pk):

    music_name = SubMusic.objects.get(id=pk).music.seed_file
    music_name = str(music_name)

    m4a2wave(music_name)
    song = AudioSegment.from_wav(PIANO_PATH + '/' + music_name)

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
