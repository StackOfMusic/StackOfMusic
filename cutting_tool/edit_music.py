import re
import os
from pydub import AudioSegment
#should change path before using this tool
PATH = "/home/junseok/jslee/capstone1/cutting_tool/source"

for path, dirs, files in os.walk(PATH):
    result_index = 300
    for filename in files:
        fullpath = os.path.join(path, filename)
        # Open file
        song = AudioSegment.from_wav(fullpath)

        # Slice audio
        # pydub uses milliseconds
        song_len = len(song)
        print(song_len)
        #one_min = ten_seconds * 6

        music_elements  = song[200:400]
        # up/down volumn
        #beginning = first_10_seconds + 6

        # Save the result
        # can give parameters-quality, channel, etc
        #beginning.exoprt('result.flac', format='flac', parameters=["-q:a", "10", "-ac", "1"])
        result_name = '{}.wav'.format(result_index)
        result_index = result_index + 1
        music_elements.export(result_name, format='wav')
