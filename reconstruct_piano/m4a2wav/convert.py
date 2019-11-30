import os
from StackOfMusic import settings
from celery import Celery
from pydub import AudioSegment

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIANO_PATH = os.path.join(BASE_DIR, 'detect_frequency')
CONVERT_PATH = os.path.join(PIANO_PATH, 'audiofile')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StackOfMusic.settings')
app = Celery('StackOfMusic')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


def m4a2wave(music_name):
    formats_to_convert = ['.m4a']
    for (dirpath, dirnames, filenames) in os.walk(settings.BASE_DIR):
        for filename in filenames:
            if filename == music_name:
                if filename.endswith(tuple(formats_to_convert)):

                    filepath = dirpath + '/' + filename
                    (path, file_extension) = os.path.splitext(filepath)
                    file_extension_final = file_extension.replace('.', '')
                    try:
                        track = AudioSegment.from_file(filepath,
                                                   file_extension_final)
                        wav_filename = filename.replace(file_extension_final, 'wav')
                        wav_path = dirpath + '/' + wav_filename
                        file_handle = track.export(wav_path, format='wav')
                        os.remove(filepath)
                    except:
                        print("ERROR CONVERTING " + str(filepath))
