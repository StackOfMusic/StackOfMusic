import re
import os
from pydub import AudioSegment

PATH = "/home/junseok/jslee/capstone1/music_source/piano"

music_source_piano = []

for path, dirs, files in os.walk(PATH):
    for filename in files:
        fullpath = os.path.join(path, filename)
        music_source = AudioSegment.from_wav(fullpath)
        music_source_piano.append(music_source)

def reconstruct_music(freq_data):
    for freq in freq_data:
        if freq > 32 and freq < 63.575:
            #1st octave
        elif freq >= 63.575 and freq < 127.145:
            #2nd octave
        elif freq >= 127.145 and freq < 254.285:
            #3rd octave
        elif freq >= 245.285 and freq < 508.57:
            #4th octave
        elif freq >= 508.57 and freq < 1017.14:
            #5th octave
        elif freq >= 1017.14 and freq < 2034.28:
            #6th octave
        elif freq >= 2034.28 and freq < 4061.92:
            #7th octave
        else :
            #out of range

