# Read in a WAV and find the freq's
import os
import pyaudio
from celery import Celery

import wave
import numpy as np
from reconstruct_piano.detect_frequency.reconstruct_music import recons_music
from reconstruct_piano.detect_frequency.edit_music import divide_music

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIANO_PATH = os.path.join(BASE_DIR, 'detect_frequency')
PIANO_RAW_PATH = os.path.join(PIANO_PATH, 'piano-raw')
MUSIC_ELEMENT_PATH = os.path.join(PIANO_PATH, 'music_element')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StackOfMusic.settings')
app = Celery('StackOfMusic')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


@app.task
def detect_freq(pk):
    divide_music(pk=pk)

    chunk = 16384
    frequency_list = []

    for path, dirs, files in os.walk(MUSIC_ELEMENT_PATH):
        sorted_files = sorted(files, key=lambda x: int(x.split('.')[0]))
        for filename in sorted_files:
            fullpath = os.path.join(path, filename)
            count = 0
            total_hz = 0.0
            # open up a wave
            wf = wave.open(fullpath, 'rb')
            swidth = wf.getsampwidth()
            RATE = wf.getframerate()
            # use a Blackman window
            window = np.blackman(chunk)
            # open stream
            p = pyaudio.PyAudio()
            stream = p.open(format =p.get_format_from_width(wf.getsampwidth()),
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
                        total_hz = total_hz + thefreq
                        count = count + 1
                else:
                    thefreq = which*RATE/chunk
                    if thefreq == thefreq:
                        total_hz = total_hz + thefreq
                        count = count + 1
                # read some more data
                data = wf.readframes(chunk)
            if count != 0:
                total_hz = total_hz / count
            frequency_list.append(total_hz)
            if data:
                stream.write(data)
            stream.close()
            p.terminate()
            os.remove(fullpath)
    recons_music(frequency_list, 0)


if __name__ == '__main__':
    detect_freq()
