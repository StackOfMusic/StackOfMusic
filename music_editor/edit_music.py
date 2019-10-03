from pydub import AudioSegment

# Open file
song = AudioSegment.from_wav('a3.wav')

# Slice audio
# pydub uses milliseconds
start_position = 200
one_seconds = 0.3 * 1000
#one_min = ten_seconds * 6

first_1_seconds = song[start_position:start_position + one_seconds]
#last_5_seconds = song[-5000:]

# up/down volumn
#beginning = first_10_seconds + 6

# Save the result
# can give parameters-quality, channel, etc
#beginning.exoprt('result.flac', format='flac', parameters=["-q:a", "10", "-ac", "1"])
first_1_seconds.export('result_a3.wav', format='wav')
