from django import forms
from music.models import Music


class CreateMusicForm(forms.ModelForm):

    class Meta:
        model = Music
        fields = (
            'genre',
            'title',
            'album_jacket',
            'music_option',
        )

    def __init__(self, *args, **kwargs):
        super(CreateMusicForm, self).__init__(*args, **kwargs)
