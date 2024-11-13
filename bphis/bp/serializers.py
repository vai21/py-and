from .models import Bp
from rest_framework import serializers


class BpSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bp
        fields = ['id', 'systolic', 'meanarterialpressure', 'pulserate', 'ihb', 'is_user_move', 'measurement_time', 'created_at', 'customer_id']
