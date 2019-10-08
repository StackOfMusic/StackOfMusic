from rest_framework import serializers
from music.models import Music


class WorkingMusicRetrieveSerializer(serializers.Serializer):

    class Meta:
        model = Music
        fields = (
            '__all__'
        )