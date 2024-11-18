from .models import Bp
from rest_framework import serializers


class BpSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bp
        fields = ['id', 'systolic', 'diastolic', 'meanarterialpressure', 'pulserate', 'ihb', 'is_user_move', 'retest', 'measurement_time', 'created_at', 'customer', 'group_id']
