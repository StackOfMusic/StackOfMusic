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
    total_like_user = serializers.IntegerField(source='total_likes_user')

    class Meta:
        model = Music
        fields = (
            'genre',
            'title',
            'seed_file',
            'album_jacket',
            'owner',
            'create_date',
            'total_like_user',
        )


class LikeMusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'liked_music'
        )
