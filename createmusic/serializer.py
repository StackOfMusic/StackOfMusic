from rest_framework import serializers
from music.models import Music, SubMusic
from instrument.models import Instrument
from StackOfMusic.serializer import UserSerializer, GenreSerializer


class InstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrument
        fields = '__all__'


class SubMusicSerializer(serializers.ModelSerializer):
    contributor = UserSerializer()
    instrument = InstrumentSerializer()

    class Meta:
        model = SubMusic
        fields = (
            'id',
            'instrument',
            'contributor',
            'music_file',
            'convert_music_file',
            'create_date',
            'status',
            'update_status',
        )


class WorkingMusicRetrieveSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    genre = GenreSerializer()
    instrument = InstrumentSerializer()
    sub_musics = SubMusicSerializer(many=True, read_only=True)

    class Meta:
        model = Music
        fields = (
            'genre',
            'title',
            'seed_file',
            'album_jacket',
            'owner',
            'create_date',
            'instrument',
            'sub_musics',
        )
