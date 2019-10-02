from rest_framework import serializers
from .models import Copyright
from music.models import Music


class CopyrightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Copyright
        fields = (
            'profit',
            'pub_data',
        )


class UserWorkingProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = (
            'title'
        )
