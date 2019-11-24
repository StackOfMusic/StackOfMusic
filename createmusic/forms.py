from django import forms
from music.models import Music, Genre, SubMusic
from instrument.models import Instrument


class CreateMusicForm(forms.ModelForm):

    class Meta:
        model = Music
        fields = (
            'genre',
            'title',
            'album_jacket',
            'seed_file',
            'instrument',
        )

    def __init__(self, music_owner, *args, **kwargs):
        self.owner = music_owner
        super(CreateMusicForm, self).__init__(*args, **kwargs)
        self.fields['genre'].queryset = Genre.objects.all()
        self.fields['instrument'].queryset = Instrument.objects.all()

    def save(self, commit=True):
        self.instance.owner = self.owner
        self.instance.music_option = 1
        self.instance.update_status = 0
        return super(CreateMusicForm, self).save(commit=commit)


class CreateSubMusicForm(forms.ModelForm):

    class Meta:
        model = SubMusic
        fields = (
            'instrument',
            'music_file',
        )

    def __init__(self, music_contributor, working_music_id, *args, **kwargs):
        self.contributor = music_contributor
        self.music = working_music_id
        super(CreateSubMusicForm, self).__init__(*args, **kwargs)
        self.fields['instrument'].queryset = Instrument.objects.all()

    def save(self, commit=True):
        self.instance.contributor = self.contributor
        self.instance.music_id = self.music
        self.instance.status = 1
        self.instance.update_status = 0
        return super(CreateSubMusicForm, self).save(commit=commit)
