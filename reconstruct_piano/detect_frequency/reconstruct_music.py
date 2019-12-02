import os

import boto3
from celery import Celery
from django.shortcuts import get_object_or_404
from pydub import AudioSegment

from StackOfMusic import settings
from music.models import SubMusic

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIANO_PATH = os.path.join(BASE_DIR, 'detect_frequency/')
AUDIO_FILE_PATH = os.path.join(PIANO_PATH, 'audiofile/')
PIANO_RAW_PATH = os.path.join(PIANO_PATH, 'piano-raw/')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StackOfMusic.settings')
app = Celery('StackOfMusic')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


def edit_source(instrument, note, length):
    filename = "{}.wav".format(note)

    music_elem_size = 400 * length
    fullpath = os.path.join(PIANO_RAW_PATH, filename)
    # Open file
    song = AudioSegment.from_wav(fullpath)

    music_source = song[100:100 + music_elem_size]
    return music_source


def recons_music(freq_data, instrument, pk):

    #instrument = 0 : piano
    reconstruct_music = AudioSegment.empty()
    #music_source = edit_source(0)
    sound_list = []
    #first = 1

    for freq in freq_data:
        #crossfade with in
        if freq >= 31.725 and freq < 63.575:
            #1st octave
            if freq >= 31.725 and freq < 33.675:
                #c1
                sound_list.append([1,0])
            elif freq >= 33.675 and freq < 35.67:
                #c1#
                sound_list.append([1,1])
            elif freq >= 35.67 and freq < 37.80:
                #d1
                sound_list.append([1,2])
            elif freq >= 37.80 and freq < 40.045:
                #d1#
                sound_list.append([1,3])
            elif freq >= 40.045 and freq < 42.425:
                #e1
                sound_list.append([1,4])
            elif freq >= 42.425 and freq < 44.95:
                #f1
                sound_list.append([1,5])
            elif freq >= 44.95 and freq < 47.625:
                #f1#
                sound_list.append([1,6])
            elif freq >= 47.625 and freq < 50.455:
                #g1
                sound_list.append([1,7])
            elif freq >= 50.455 and freq < 53.455:
                #g1#
                sound_list.append([1,8])
            elif freq >= 53.455 and freq < 56.635:
                #a1
                sound_list.append([1,9])
            elif freq >= 56.635 and freq < 60.005:
                #a1#
                sound_list.append([1,10])
            else:
                #b1
                sound_list.append([1,11])
        elif freq >= 63.575 and freq < 127.145:
            #2nd octave
            if freq >= 63.575 and freq < 67.355:
                #c2
                sound_list.append([2,0])
            elif freq >= 67.355 and freq < 71.36:
                #c2#
                sound_list.append([2,1])
            elif freq >= 71.36 and freq < 75.60:
                #d2
                sound_list.append([2,2])
            elif freq >= 75.60 and freq < 80.095:
                #d2#
                sound_list.append([2,3])
            elif freq >= 80.095 and freq < 84.86:
                #e2
                sound_list.append([2,4])
            elif freq >= 84.86 and freq < 89.905:
                #f2
                sound_list.append([2,5])
            elif freq >= 89.905 and freq < 95.25:
                #f2#
                sound_list.append([2,6])
            elif freq >= 95.35 and freq < 100.915:
                #g2
                sound_list.append([2,7])
            elif freq >= 100.915 and freq < 106.915:
                #g2#
                sound_list.append([2,8])
            elif freq >= 106.915 and freq < 113.27:
                #a2
                sound_list.append([2,9])
            elif freq >= 113.27 and freq < 120.005:
                #a2#
                sound_list.append([2,10])
            else :
                #b2
                sound_list.append([2,11])
        elif freq >= 127.145 and freq < 254.285:
            #3rd octave
            if freq >= 127.145 and freq < 134.705:
                #c3
                sound_list.append([3,0])
            elif freq >= 134.705 and freq < 142.71:
                #c3#
                sound_list.append([3,1])
            elif freq >= 142.71 and freq < 151.20:
                #d3
                sound_list.append([3,2])
            elif freq >= 151.20 and freq < 160.195:
                #d3#
                sound_list.append([3,3])
            elif freq >= 160.195 and freq < 169.72:
                #e3
                sound_list.append([3,4])
            elif freq >= 169.72 and freq < 179.81:
                #f3
                sound_list.append([3,5])
            elif freq >= 179.81 and freq < 190.50:
                #f3#
                sound_list.append([3,6])
            elif freq >= 190.50 and freq < 201.825:
                #g3
                sound_list.append([3,7])
            elif freq >= 201.825 and freq < 213.825:
                #g3#
                sound_list.append([3,8])
            elif freq >= 213.825 and freq < 226.54:
                #a3
                sound_list.append([3,9])
            elif freq >= 226.54 and freq < 240.01:
                #a3#
                sound_list.append([3,10])
            else :
                #b3
                sound_list.append([3,11])
        elif freq >= 254.285 and freq < 508.57:
            #4th octave
            if freq >= 254.285 and freq < 269.405:
                #c4
                sound_list.append([4,0])
            elif freq >= 269.405 and freq < 285.42:
                #c4#
                sound_list.append([4,1])
            elif freq >= 285.42 and freq < 302.395:
                #d4
                sound_list.append([4,2])
            elif freq >= 302.395 and freq < 320.38:
                #d4#
                sound_list.append([4,3])
            elif freq >= 320.38 and freq < 339.43:
                #e4
                sound_list.append([4,4])
            elif freq >= 339.43 and freq < 359.61:
                #f4
                sound_list.append([4,5])
            elif freq >= 359.61 and freq < 380.995:
                #f4#
                sound_list.append([4,6])
            elif freq >= 380.995 and freq < 403.65:
                #g4
                sound_list.append([4,7])
            elif freq >= 403.65 and freq < 427.65:
                #g4#
                sound_list.append([4,8])
            elif freq >= 427.65 and freq < 453.08:
                #a4
                sound_list.append([4,9])
            elif freq >= 453.08 and freq < 480.02:
                #a4#
                sound_list.append([4,10])
            else:
                #b4
                sound_list.append([4,11])
        elif freq >= 508.57 and freq < 1017.14:
            #5th octave
            if freq >= 508.57 and freq < 538.81:
                #c5
                sound_list.append([5,0])
            elif freq >= 538.81 and freq < 570.84:
                #c5#
                sound_list.append([5,1])
            elif freq >= 570.84 and freq < 604.79:
                #d5
                sound_list.append([5,2])
            elif freq >= 604.79 and freq < 640.76:
                #d5#
                sound_list.append([5,3])
            elif freq >= 640.76 and freq < 678.86:
                #e5
                sound_list.append([5,4])
            elif freq >= 678.85 and freq < 719.22:
                #f5
                sound_list.append([5,5])
            elif freq >= 719.22 and freq < 761.99:
                #f5#
                sound_list.append([5,6])
            elif freq >= 761.99 and freq < 807.30:
                #g5
                sound_list.append([5,7])
            elif freq >= 807.30 and freq < 855.30:
                #g5#
                sound_list.append([5,8])
            elif freq >= 855.30 and freq < 906.16:
                #a5
                sound_list.append([5,9])
            elif freq >= 906.16 and freq < 960.04:
                #a5#
                sound_list.append([5,10])
            else :
                #b5
                sound_list.append([5,11])
        elif freq >= 1017.14 and freq < 2034.28:
            #6th octave
            if freq >= 1017.14 and freq < 1077.62:
                #c6
                sound_list.append([6,0])
            elif freq >= 1077.62 and freq < 1141.68:
                #c6#
                sound_list.append([6,1])
            elif freq >= 1141.68 and freq < 1209.58:
                #d6
                sound_list.append([6,2])
            elif freq >= 1209.58 and freq < 1281.52:
                #d6#
                sound_list.append([6,3])
            elif freq >= 1281.52 and freq < 1357.72:
                #e6
                sound_list.append([6,4])
            elif freq >= 1357.72 and freq < 1438.44:
                #f6
                sound_list.append([6,5])
            elif freq >= 1438.44 and freq < 1523.98:
                #f6#
                sound_list.append([6,6])
            elif freq >= 1523.98 and freq < 1614.60:
                #g6
                sound_list.append([6,7])
            elif freq >= 1614.60 and freq < 1710.60:
                #g6#
                sound_list.append([6,8])
            elif freq >= 1710.60 and freq < 1812.32:
                #a6
                sound_list.append([6,9])
            elif freq >= 1812.32 and freq < 1920.08:
                #a6#
                sound_list.append([6,10])
            else :
                #b6
                sound_list.append([6,11])
        elif freq >= 2034.28 and freq < 4061.92:
            #7th octave
            if freq >= 2034.28 and freq < 2155.24:
                #c7
                sound_list.append([7,0])
            elif freq >= 2155.24 and freq < 2283.36:
                #c7#
                sound_list.append([7,1])
            elif freq >= 2283.36 and freq < 2419.16:
                #d7
                sound_list.append([7,2])
            elif freq >= 2419.26 and freq < 2563.04:
                #d7#
                sound_list.append([7,3])
            elif freq >= 2563.04 and freq < 2715.44:
                #e7
                sound_list.append([7,4])
            elif freq >= 2715.44 and freq < 2876.88:
                #f7
                sound_list.append([7,5])
            elif freq >= 2876.88 and freq < 3047.96:
                #f7#
                sound_list.append([7,6])
            elif freq >= 3047.96 and freq < 3229.20:
                #g7
                sound_list.append([7,7])
            elif freq >= 3229.20 and freq < 3421.20:
                #g7#
                sound_list.append([7,8])
            elif freq >= 3421.20 and freq < 3624.64:
                #a7
                sound_list.append([7,9])
            elif freq >= 3624.64 and freq < 3840.16:
                #a7#
                sound_list.append([7,10])
            else :
                #b7
                sound_list.append([7,11])
        else :
            pass
    print('hi! last')
    for sound in sound_list:
        note = sound[0] * 100 + sound[1]
        reconstruct_music = reconstruct_music + edit_source(0, note, 1)

    music_name = get_object_or_404(SubMusic, pk=pk).music_file.name
    music_name = os.path.splitext(music_name)[0]
    music_name = music_name.replace('audiofile/', '')
    reconstruct_music.export(PIANO_PATH + 'new_' + music_name + '.wav', format='wav')
    file_save(pk, music_name)


def file_save(pk, music_name):

    submusic_path = os.path.join(PIANO_PATH, 'new_' + music_name + '.wav')
    with open(submusic_path, 'rb') as f:
        contents = f.read()

    submusic = get_object_or_404(SubMusic, pk=pk)
    submusic.update_status = 2
    submusic.convert_music_file.name = 'new_' + music_name + '.wav'
    s3 = boto3.resource(
        's3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    bucket = s3.Bucket('stackofmusic')
    bucket.put_object(Key=submusic.convert_music_file.name, Body=contents)

    submusic.update_status = 2
    submusic.save()
    os.remove(settings.BASE_DIR + '/' + music_name + '.wav')
    os.remove(submusic_path)
