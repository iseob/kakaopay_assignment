from rest_framework import serializers
from stats import models
from core.common import device_name_map


class StatSerializer(serializers.ModelSerializer):
    device_name = serializers.SerializerMethodField(source='device_name')
    rate = serializers.SerializerMethodField(source='device_usage_rate')

    def get_device_name(self, obj):
        _device_name = device_name_map[obj.device_name]
        return _device_name

    def get_rate(self, obj):
        return obj.device_usage_rate

    class Meta:
        model = models.Stat
        fields = ('year', 'rate', 'device_name')
