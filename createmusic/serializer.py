from rest_framework import serializers
from music.models import Music
from StackOfMusic.serializer import UserSerializer, GenreSerializer


class WorkingMusicRetrieveSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    genre = GenreSerializer()

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
        )
