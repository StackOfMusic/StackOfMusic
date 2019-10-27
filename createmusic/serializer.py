from rest_framework import serializers
from music.models import Music, SubMusic
from StackOfMusic.serializer import UserSerializer, GenreSerializer


class SubMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMusic
        fields = '__all__'


class WorkingMusicRetrieveSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    genre = GenreSerializer()
    sub_music = SubMusicSerializer(many=True, read_only=True)

    class Meta:
        model = Music
        fields = (
            'genre',
            'title',
            'seed_file',
            'album_jacket',
            'owner',
            'create_date',
            'like',
            'sub_music',
        )
