from pydub import AudioSegment

# Open file
song = AudioSegment.from_wav('./source/airplane.wav')

# Slice audio
# pydub uses milliseconds
elements = 0
result_index = 0
song_len = len(song)
element_size = 400
#one_min = ten_seconds * 6

while elements < song_len:
    if elements + element_size < song_len:
        music_elements  = song[elements:elements + element_size]
    else:
        music_elements = song[elements:song_len]
    elements = elements + element_size
#last_5_seconds = song[-5000:]

# up/down volumn
#beginning = first_10_seconds + 6

# Save the result
# can give parameters-quality, channel, etc
#beginning.exoprt('result.flac', format='flac', parameters=["-q:a", "10", "-ac", "1"])
    result_name = '{}.wav'.format(result_index)
    result_index = result_index + 1
    music_elements.export(result_name, format='wav')
