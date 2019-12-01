from rest_framework import serializers

from music.models import Music, Comment, Genre
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
        )


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = (
            'user',
            'comment_text',
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
    comment = CommentSerializer(many=True)
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
            'comment',
        )


class LikeMusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'liked_music'
        )
