import os
import wave

import boto3
import librosa
import numpy as np
import pyaudio
from celery import Celery
from django.shortcuts import get_object_or_404
from pydub import AudioSegment

from StackOfMusic import settings
from music.models import SubMusic
from reconstruct_piano.detect_frequency.edit_music import s3_file_download
from reconstruct_piano.m4a2wav.convert import m4a2wave

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRUM_PATH = os.path.join(BASE_DIR, 'reconstruct_drum/')
MUSIC_SEG_PATH = os.path.join(DRUM_PATH, 'music_seg/')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StackOfMusic.settings')
app = Celery('StackOfMusic')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


def divide_sound(fullpath, hit_point, pk):

    song = AudioSegment.from_wav(fullpath)

    result_index = 0
    segment_len = 400
    song_len = len(song)

    for point in hit_point:
        elements = point - segment_len/2
        if elements + segment_len < song_len:
            music_elements = song[elements:elements + segment_len]
        else:
            music_elements = song[elements:song_len]

        result_name = MUSIC_SEG_PATH + '{}.wav'.format(result_index)
        result_index = result_index + 1
        music_elements.export(result_name, format='wav')

    return song_len


def detect_freq():
    chunk = 16384
    drum_list = []
    count = 0

    for path, dirs, files in os.walk(MUSIC_SEG_PATH):
        sorted_files = sorted(files, key=lambda x: int(x.split('.')[0]))
        for filename in sorted_files:
            fullpath = os.path.join(path, filename)
            freq_list = []
            # open up a wave
            wf = wave.open(fullpath, 'rb')
            swidth = wf.getsampwidth()
            RATE = wf.getframerate()
            # use a Blackman window
            window = np.blackman(chunk)
            # open stream
            p = pyaudio.PyAudio()
            stream = p.open(format =
                            p.get_format_from_width(wf.getsampwidth()),
                            channels = wf.getnchannels(),
                            rate = RATE,
                            output = True)

            # read some data
            data = wf.readframes(chunk)
            # play stream and find the frequency of each chunk
            while len(data) == chunk*swidth:
                # write data out to the audio stream

                # unpack the data and times by the hamming window
                indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth), data))*window
                # Take the fft and square each value
                fftData=abs(np.fft.rfft(indata))**2
                # find the maximum
                which = fftData[1:].argmax() + 1
                # use quadratic interpolation around the max
                if which != len(fftData)-1:
                    y0,y1,y2 = np.log(fftData[which-1:which+2:])
                    x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                    # find the frequency and output it
                    thefreq = (which+x1)*RATE/chunk
                    if thefreq == thefreq:
                        freq_list.append(thefreq)
                else:
                    thefreq = which*RATE/chunk
                    if thefreq == thefreq:
                        freq_list.append(thefreq)
                # read some more data
                data = wf.readframes(chunk)
            count += 1
            if data:
                pass
            stream.close()
            p.terminate()

            bass_cnt = 0
            snare_cnt = 0
            hi_hat_cnt = 0

            for freq in freq_list:
                if freq > 40 and freq < 130:
                    snare_cnt += 1
                elif freq > 130 and freq < 200:
                    bass_cnt += 1
                elif freq > 4000 and freq < 7000:
                    hi_hat_cnt += 1
                else:
                    pass
            
            max_val = max([bass_cnt, snare_cnt, hi_hat_cnt])
            if bass_cnt == max_val:
                drum_list.append(0)
            elif snare_cnt == max_val:
                drum_list.append(1)
            else:
                drum_list.append(2)

            os.remove(fullpath)

    return drum_list


def reconstruct_beat(sound_list, hit_point, time_gap, beat_num):
    segment_len = 400
    half_len = segment_len / 2
    sample_sound = []
    path = os.path.join(DRUM_PATH, 'drum_sample')
    fullpath = os.path.join(path, 'bass_sample.wav')
    sample = AudioSegment.from_wav(fullpath)
    sample_sound.append(sample[2000 - (segment_len/2):2000 + (segment_len/2)])
    fullpath = os.path.join(path, 'snare_sample.wav')
    sample = AudioSegment.from_wav(fullpath)
    sample_sound.append(sample[2000 - (segment_len/2):2000 + (segment_len/2)])
    fullpath = os.path.join(path, 'hi_hat_sample.wav')
    sample = AudioSegment.from_wav(fullpath)
    sample_sound.append(sample[2000 - (segment_len/2):2000 + (segment_len/2)])

    new_sound = sample_sound[sound_list[0]]

    beat_count = 1
    bass_cnt = 0
    snare_cnt = 0
    hihat_cnt = 0
    for i in range(1, len(sound_list)):
        new_sound = new_sound + AudioSegment.silent(duration = time_gap - half_len)
        new_sound = new_sound + sample_sound[sound_list[i]]
        if sound_list[i] == 0:
            bass_cnt += 1
        elif sound_list[i] == 1:
            snare_cnt += 1
        else:
            hihat_cnt += 1
        beat_count += 1

    max_cnt = max(bass_cnt, snare_cnt, hihat_cnt)
    max_sound = 0
    if max_cnt == bass_cnt:
        max_sound = 0
    elif max_cnt == snare_cnt:
        max_sound = 1
    else:
        max_sound = 2

    while beat_count < beat_num:
        new_sound = new_sound + AudioSegment.silent(duration = time_gap - half_len)
        new_sound = new_sound + sample_sound[max_sound]
        beat_count += 1

    new_sound = new_sound + AudioSegment.silent(duration = time_gap - half_len)

    return new_sound


@app.task
def detect_beat(pk):

    s3_file_download(pk)
    music_name = get_object_or_404(SubMusic, pk=pk).music_file.name

    music_name = music_name.replace('audiofile/', '')
    m4a2wave(music_name)
    music_name = os.path.splitext(music_name)[0]
    music_name = music_name + '.wav'

    path = settings.BASE_DIR

    filename = music_name
    fullpath = os.path.join(path, filename)

    y, sr = librosa.load(fullpath)
    tempo, beats = librosa.beat.beat_track(y = y, sr = sr)
    frame2time_raw = librosa.frames_to_time(beats, sr = sr)

    frame2time = []
    for x in np.nditer(frame2time_raw):
        frame2time.append(round(x * 1000))

    beat_len = len(frame2time)
    beat_num = 1
    stop = False

    while stop == False:
        if beat_num < beat_len:
            beat_num = beat_num * 2
        else:
            stop = True

    segment_len = round((60 / tempo) * 1000)
    song_len = divide_sound(fullpath, frame2time, pk)
    sound_list = detect_freq()
    new_sound = reconstruct_beat(sound_list, frame2time, segment_len, beat_num)

    new_sound.export('new_' + music_name, format='wav')
    drum_file_save(pk, music_name)


def drum_file_save(pk, music_name):

    submusic_path = os.path.join(settings.BASE_DIR, 'new_' + music_name)
    with open(submusic_path, 'rb') as f:
        contents = f.read()

    submusic = get_object_or_404(SubMusic, pk=pk)
    submusic.update_status = 2
    submusic.convert_music_file.name = 'audiofile/' + 'new_' + music_name
    s3 = boto3.resource(
        's3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    bucket = s3.Bucket('stackofmusic')
    bucket.put_object(Key=submusic.convert_music_file.name, Body=contents)

    submusic.update_status = 2
    submusic.save()
    os.remove(submusic_path)
