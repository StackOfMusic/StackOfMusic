from django import forms
from music.models import Music


class CreateMusicForm(forms.ModelForm):

    class Meta:
        model = Music
        fields = (
            'genre',
            'title',
            'album_jacket',
            'seed_file',
        )

    def __init__(self, music_owner, *args, **kwargs):
        self.owner = music_owner
        super(CreateMusicForm, self).__init__(*args, **kwargs)
        self.fields['album_jacket'].required = False

    def save(self, commit=True):
        self.instance.owner = self.owner
        self.instance.music_option = 1
        return super(CreateMusicForm, self).save(commit=commit)
