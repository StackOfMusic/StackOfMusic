import re
import os
import pyaudio
import librosa
import math
import wave
import numpy as np
from pydub import AudioSegment
from music.models import SubMusic

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRUM_PATH = os.path.join(BASE_DIR, 'reconstruct_drum/')
MUSIC_SEG_PATH = os.path.join(DRUM_PATH, 'music_seg/')


def divide_sound(fullpath, hit_point):
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


def reconstruct_beat(sound_list, hit_point, song_len):
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
  
    start_gap = 0
    new_sound = AudioSegment.empty()
    if hit_point[0] - half_len >= 0:
        start_gap = hit_point[0] - half_len
        new_sound = AudioSegment.silent(duration = start_gap)
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


def detect_beat(pk):
    path = os.path.join(DRUM_PATH, 'data')
    filename = SubMusic.objects.get(id=pk).music_file

    fullpath = os.path.join(path, filename)

    y, sr = librosa.load(fullpath)
    tempo, beats = librosa.beat.beat_track(y = y, sr = sr)
    frame2time_raw = librosa.frames_to_time(beats, sr = sr)

    frame2time = []
    for x in np.nditer(frame2time_raw):
        frame2time.append(round(x * 1000))

    segment_len = round((60 / tempo) * 1000)
    song_len = divide_sound(fullpath, frame2time)
    sound_list = detect_freq()
    new_sound = reconstruct_beat(sound_list, frame2time, song_len)

    new_sound.export('new_music.wav', format='wav')


# if __name__ == "__main__":
#     detect_beat(pk=pk)
