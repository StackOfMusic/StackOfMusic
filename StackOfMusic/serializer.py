from rest_framework import serializers
from music.models import Music


class CompletedMusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = (
            'genre',
            'title',
            'seed_file',
            'album_jacket',
        )
