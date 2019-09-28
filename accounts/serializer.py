from rest_framework import serializers
from .models import Copyright


class CopyrightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Copyright
        fields = (
            'profit',
        )
