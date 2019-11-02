from rest_framework import serializers
from instrument.models import Instrument


class InstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrument
        fields = (
            'name'
        )
