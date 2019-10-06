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
        if freq >= 31.725 and freq < 63.575:
            #1st octave
            if freq >= 31.725 and freq < 33.675:
                #c1
            elif freq >= 33.675 and freq < 35.67:
                #c1#
            elif freq >= 35.67 and freq < 37.80:
                #d1
            elif freq >= 37.80 and freq < 40.045:
                #d1#
            elif freq >= 40.045 and freq < 42.425:
                #e1
            elif freq >= 42.425 and freq < 44.95:
                #f1
            elif freq >= 44.95 and freq < 47.625:
                #f1#
            elif freq >= 47.625 and freq < 50.455:
                #g1
            elif freq >= 50.455 and freq < 53.455:
                #g1#
            elif freq >= 53.455 and freq < 56.635:
                #a1
            elif freq >= 56.635 and freq < 60.005:
                #a1#
            else:
                #b1
        elif freq >= 63.575 and freq < 127.145:
            #2nd octave
            if freq >= 63.575 and freq < 67.355:
                #c2
            elif freq >= 67.355 and freq < 71.36:
                #c2#
            elif freq >= 71.36 and freq < 75.60:
                #d2
            elif freq >= 75.60 and freq < 80.095:
                #d2#
            elif freq >= 80.095 and freq < 84.86:
                #e2
            elif freq >= 84.86 and freq < 89.905:
                #f2
            elif freq >= 89.905 and freq < 95.25:
                #f2#
            elif freq >= 95.35 and freq < 100.915:
                #g2
            elif freq >= 100.915 and freq < 106.915:
                #g2#
            elif freq >= 106.915 and freq < 113.27:
                #a2
            elif freq >= 113.27 and freq < 120.005:
                #a2#
            else :
                #b2
        elif freq >= 127.145 and freq < 254.285:
            #3rd octave
            if freq >= 127.145 and freq < 134.705:
                #c3
            elif freq >= 134.705 and freq < 142.71:
                #c3#
            elif freq >= 142.71 and freq < 151.20:
                #d3
            elif freq >= 151.20 and freq < 160.195:
                #d3#
            elif freq >= 160.195 and freq < 169.72:
                #e3
            elif freq >= 169.72 and freq < 179.81:
                #f3
            elif freq >= 179.81 and freq < 190.50:
                #f3#
            elif freq >= 190.50 and freq < 201.825:
                #g3
            elif freq >= 201.825 and freq < 213.825:
                #g3#
            elif freq >= 213.825 and freq < 226.54:
                #a3
            elif freq >= 226.54 and freq < 240.01:
                #a3#
            else :
                #b3
        elif freq >= 254.285 and freq < 508.57:
            #4th octave
            if freq >= 254.285 and freq < 269.405:
                #c4
            elif freq >= 269.405 and freq < 285.42:
                #c4#
            elif freq >= 285.42 and freq < 302.395:
                #d4
            elif freq >= 302.395 and freq < 320.38:
                #d4#
            elif freq >= 320.38 and freq < 339.43:
                #e4
            elif freq >= 339.43 and freq < 359.61:
                #f4
            elif freq >= 359.61 and freq < 380.995:
                #f4#
            elif freq >= 380.995 and freq < 403.65:
                #g4
            elif freq >= 403.65 and freq < 427.65:
                #g4#
            elif freq >= 427.65 and freq < 453.08:
                #a4
            elif freq >= 453.08 and freq < 480.02:
                #a4#
            else:
                #b4
        elif freq >= 508.57 and freq < 1017.14:
            #5th octave
            if freq >= 508.57 and freq < 538.81:
                #c5
            elif freq >= 538.81 and freq < 570.84:
                #c5#
            elif freq >= 570.84 and freq < 604.79:
                #d5
            elif freq >= 604.79 and freq < 640.76:
                #d5#
            elif freq >= 640.76 and freq < 678.86:
                #e5
            elif freq >= 678.85 and freq < 719.22:
                #f5
            elif freq >= 719.22 and freq < 761.99:
                #f5#
            elif freq >= 761.99 and freq < 807.30:
                #g5
            elif freq >= 807.30 and freq < 855.30:
                #g5#
            elif freq >= 855.30 and freq < 906.16:
                #a5
            elif freq >= 906.16 and freq < 960.04:
                #a5#
            else :
                #b5
        elif freq >= 1017.14 and freq < 2034.28:
            #6th octave
            if freq >= 1017.14 and freq < 1077.62:
                #c6
            elif freq >= 1077.62 and freq < 1141.68:
                #c6#
            elif freq >= 1141.68 and freq < 1209.58:
                #d6
            elif freq >= 1209.58 and freq < 1281.52:
                #d6#
            elif freq >= 1281.52 and freq < 1357.72:
                #e6
            elif freq >= 1357.72 and freq < 1438.44:
                #f6
            elif freq >= 1438.44 and freq < 1523.98:
                #f6#
            elif freq >= 1523.98 and freq < 1614.60:
                #g6
            elif freq >= 1614.60 and freq < 1710.60:
                #g6#
            elif freq >= 1710.60 and freq < 1812.32:
                #a6
            elif freq >= 1812.32 and freq < 1920.08:
                #a6#
            else :
                #b6
        elif freq >= 2034.28 and freq < 4061.92:
            #7th octave
            if freq >= 2034.28 and freq < 2155.24:
                #c7
            elif freq >= 2155.24 and freq < 2283.36:
                #c7#
            elif freq >= 2283.36 and freq < 2419.16:
                #d7
            elif freq >= 2419.26 and freq < 2563.04:
                #d7#
            elif freq >= 2563.04 and freq < 2715.44:
                #e7
            elif freq >= 2715.44 and freq < 2876.88:
                #f7
            elif freq >= 2876.88 and freq < 3047.96:
                #f7#
            elif freq >= 3047.96 and freq < 3229.20:
                #g7
            elif freq >= 3229.20 and freq < 3421.20:
                #g7#
            elif freq >= 3421.20 and freq < 3624.64:
                #a7
            elif freq >= 3624.64 and freq < 3840.16:
                #a7#
            else :
                #b7
        else :
            #out of range

