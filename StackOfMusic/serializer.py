from rest_framework import serializers

from music.models import Music
from music.models import Genre
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
        )


class CompletedMusicSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    genre = GenreSerializer()
    # contributor = UserSrializer()

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



    # def save(self, commit=True):
    #     self.owner =
    #     self.contributor =
    #     self.genre =
    #     return super(CompletedMusicSerializer, self).save(commit=commit)
