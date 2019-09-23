from rest_framework import serializers
from devices import models


class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device
        fields = ('id', 'device_id', 'device_name',)

