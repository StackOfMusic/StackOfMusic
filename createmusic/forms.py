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

    def __init__(self, music_owner, *args, **kwargs):
        self.owner = music_owner
        super(CreateMusicForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.owner = self.owner
        return super(CreateMusicForm, self).save(commit=commit)
