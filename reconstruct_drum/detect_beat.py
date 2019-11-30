import os
import wave

import boto3
import librosa
import numpy as np
import pyaudio
from celery import Celery
from django.shortcuts import get_object_or_404
from pydub import AudioSegment

<<<<<<< HEAD
def divide_sound(fullpath, hit_point, PK):
=======
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

>>>>>>> 28664ba351b26ec29e7b254ea35d0a042756359d
    song = AudioSegment.from_wav(fullpath)

    result_index = 0
    segment_len = 200
    song_len = len(song)

    save_dir = '/home/junseok/jslee/capstone1/StackOfMusic/reconstruct_drum/music_seg/'
    save_dir = save_dir + PK

    for point in hit_point:
        elements = point - segment_len/2
        if elements + segment_len < song_len:
            music_elements = song[elements:elements + segment_len]
        else:
            music_elements = song[elements:song_len]

<<<<<<< HEAD
        result_name = save_dir + '{}.wav'.format(result_index)
        result_index += 1
=======
        result_name = MUSIC_SEG_PATH + '{}.wav'.format(result_index)
        result_index = result_index + 1
>>>>>>> 28664ba351b26ec29e7b254ea35d0a042756359d
        music_elements.export(result_name, format='wav')

    return song_len

<<<<<<< HEAD
def detect_freq(PK):
    chunk = 8192
    drum_list = []
    count = 0;

    PATH = "/home/junseok/jslee/capstone1/StackOfMusic/reconstruct_drum/music_seg"

    for path, dirs, files in os.walk(PATH):
        handled_files = []
        for single_file in files:
            if PK in single_file:
                handled_files.append(single_file.replace(PK, ''))
        sorted_files = sorted(handled_files, key=lambda x: int(x.split('.')[0]))
        bass_next = 0
        snare_next = 1
        hi_hat_next = 2
        sound_buff = 0
=======

def detect_freq():
    chunk = 16384
    drum_list = []
    count = 0

    for path, dirs, files in os.walk(MUSIC_SEG_PATH):
        sorted_files = sorted(files, key=lambda x: int(x.split('.')[0]))
>>>>>>> 28664ba351b26ec29e7b254ea35d0a042756359d
        for filename in sorted_files:
            filename = PK + filename
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
                stream.write(data)
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
                stream.write(data)
            stream.close()
            p.terminate()

            bass_cnt = 0
            snare_cnt = 0
            hi_hat_cnt = 0

            for freq in freq_list:
                if freq > 40 and freq < 120:
                    snare_cnt += 1
                elif freq > 120 and freq < 200:
                    bass_cnt += 1
                elif freq > 4000 and freq < 7000:
                    hi_hat_cnt += 1
                else:
                    pass
            
            max_val = max([bass_cnt, snare_cnt, hi_hat_cnt])
            if max_val != 0:
                if bass_cnt == max_val:
                    drum_list.append(0)
                    if sound_buff == 0:
                        bass_next = 0
                    elif sound_buff == 1:
                        snare_next = 0
                    elif sound_buff == 2:
                        hi_hat_next = 0
                    else:
                        pass
                    sound_buff = 0
                elif snare_cnt == max_val:
                    drum_list.append(1)
                    if sound_buff == 0:
                        bass_next = 1
                    elif sound_buff == 1:
                        snare_next = 1
                    elif sound_buff == 2:
                        hi_hat_next = 1
                    else:
                        pass
                    sound_buff = 1
                else:
                    drum_list.append(2)
                    if sound_buff == 0:
                        bass_next = 2
                    elif sound_buff == 1:
                        snare_next = 2
                    elif sound_buff == 2:
                        hi_hat_next = 2
                    else:
                        pass
                    sound_buff = 2
            else:
                if sound_buff == 0:
                    drum_list.append(bass_next)
                elif sound_buff == 1:
                    drum_list.append(snare_next)
                elif sound_buff == 2:
                    drum_list.append(hi_hat_next)
                else:
                    pass
            os.remove(fullpath)

    return drum_list


def reconstruct_beat(sound_list, hit_point, song_len):
    segment_len = 200
    half_len = segment_len / 2
    sample_sound = []
<<<<<<< HEAD
    path = "/home/junseok/jslee/capstone1/StackOfMusic/reconstruct_drum/drum_sample"
=======
    path = os.path.join(DRUM_PATH, 'drum_sample')
>>>>>>> 28664ba351b26ec29e7b254ea35d0a042756359d
    fullpath = os.path.join(path, 'bass_sample.wav')
    sample = AudioSegment.from_wav(fullpath)
    sample_sound.append(sample[2000 - (segment_len/2):2000 + (segment_len/2)])
    fullpath = os.path.join(path, 'snare_sample.wav')
    sample = AudioSegment.from_wav(fullpath)
    sample_sound.append(sample[2000 - (segment_len/2):2000 + (segment_len/2)])
    fullpath = os.path.join(path, 'hi_hat_sample.wav')
    sample = AudioSegment.from_wav(fullpath)
    sample_sound.append(sample[2000 - (segment_len/2):2000 + (segment_len/2)])
  
    start_gap = 0
    new_sound = AudioSegment.empty()
    if hit_point[0] - half_len >= 0:
        start_gap = hit_point[0] - half_len
        new_sound = AudioSegment.silent(duration = start_gap)
        new_sound = new_sound + sample_sound[sound_list[0]]
    else:
        start_gap = 0
        new_sound = sample_sound[sound_list[0]]
    for i in range(1, len(sound_list)):
        temp_gap = hit_point[i] - half_len - hit_point[i-1] - half_len
        if temp_gap > 0:
            new_sound = new_sound + AudioSegment.silent(duration = temp_gap) + sample_sound[sound_list[i]]
        else:
            new_sound = new_sound + sample_sound[sound_list[i]]

    return new_sound
<<<<<<< HEAD
   
def detect_beat():
    path = "/home/junseok/jslee/capstone1/StackOfMusic/reconstruct_drum/data"
    filename = "drum6.wav"
    #PK is the string to distinguish process#################
    PK = 'test'
=======
>>>>>>> 28664ba351b26ec29e7b254ea35d0a042756359d


@app.task
def detect_beat(pk):

    s3_file_download(pk)
    music_name = get_object_or_404(SubMusic, pk=pk).music_file.name

    music_name = music_name[10:]
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

    segment_len = round((60 / tempo) * 1000)
<<<<<<< HEAD
    song_len = divide_sound(fullpath, frame2time, PK)
    sound_list = detect_freq(PK)
=======
    song_len = divide_sound(fullpath, frame2time, pk)
    sound_list = detect_freq()
>>>>>>> 28664ba351b26ec29e7b254ea35d0a042756359d
    new_sound = reconstruct_beat(sound_list, frame2time, song_len)

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
