from pydub import AudioSegment

def divide_music():
    song = AudioSegment.from_wav('./source/butterfly.wav')

    start_postion = 2000
    elements = 0 + 2000
    result_index = 0
    song_len = len(song)
    element_size = 400

    while elements < song_len:
        if elements + element_size < song_len:
            music_elements  = song[elements:elements + element_size]
        else:
            music_elements = song[elements:song_len]
        elements = elements + element_size

        result_name = '/home/junseok/jslee/capstone1/reconstruct_piano/detect_frequency/music_element/{}.wav'.format(result_index)
        result_index = result_index + 1
        music_elements.export(result_name, format='wav')
