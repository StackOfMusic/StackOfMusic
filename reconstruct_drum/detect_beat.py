import re
import os
import pyaudio
import librosa
import math
import wave
import numpy as np
from pydub import AudioSegment

def divide_sound(fullpath, hit_point, PK):
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

        result_name = save_dir + '{}.wav'.format(result_index)
        result_index += 1
        music_elements.export(result_name, format='wav')

    return song_len

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
        for filename in sorted_files:
            filename = PK + filename
            fullpath = os.path.join(path, filename)
            freq_list = []
            print("file start!!!!!!!!!")
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
                indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth), \
                                                     data))*window
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
                    print ('count: {} The freq is {} Hz.'.format(count, thefreq))
                else:
                    thefreq = which*RATE/chunk
                    if thefreq == thefreq:
                        freq_list.append(thefreq)
                    print ('count: {} The freq is {} Hz.'.format(count, thefreq))
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
    path = "/home/junseok/jslee/capstone1/StackOfMusic/reconstruct_drum/drum_sample"
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
   
def detect_beat():
    path = "/home/junseok/jslee/capstone1/StackOfMusic/reconstruct_drum/data"
    filename = "drum6.wav"
    #PK is the string to distinguish process#################
    PK = 'test'

    fullpath = os.path.join(path, filename)
    y, sr = librosa.load(fullpath)
    tempo, beats = librosa.beat.beat_track(y = y, sr = sr)
    frame2time_raw = librosa.frames_to_time(beats, sr = sr)

    frame2time = []
    for x in np.nditer(frame2time_raw):
        frame2time.append(round(x * 1000))
    print(frame2time)

    segment_len = round((60 / tempo) * 1000)
    song_len = divide_sound(fullpath, frame2time, PK)
    sound_list = detect_freq(PK)
    new_sound = reconstruct_beat(sound_list, frame2time, song_len)

    new_sound.export('new_music.wav', format='wav')



    

if __name__ == "__main__":
    detect_beat()
