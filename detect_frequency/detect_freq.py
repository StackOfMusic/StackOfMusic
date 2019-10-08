# Read in a WAV and find the freq's
import os
import pyaudio
import wave
import numpy as np
from reconstruct_music import recons_music


def detect_freq():
    chunk = 2048
    frequency_list = []

    PATH = "/home/junseok/jslee/capstone1/detect_frequency/music_element"

    for path, dirs, files in os.walk(PATH):
        for filename in files:
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
                        total_hz = total_hz + thefreq
                        count = count + 1
                    print ('The freq is {} Hz.'.format(thefreq))
                else:
                    thefreq = which*RATE/chunk
                    if thefreq == thefreq:
                        total_hz = total_hz + thefreq
                        count = count + 1
                    print ('The freq is {} Hz.'.format(thefreq))
                # read some more data
                data = wf.readframes(chunk)
            if count != 0:
                total_hz = total_hz / count
            frequency_list.append(total_hz)
            print('average freq is {} Hz.'.format(total_hz))
            if data:
                stream.write(data)
            stream.close()
            p.terminate()

    recons_music(frequency_list, 0)


if __name__ == '__main__':
    detect_freq()
