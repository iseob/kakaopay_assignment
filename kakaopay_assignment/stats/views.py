from rest_framework import viewsets
from devices.models import Device
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from stats.serializers import StatSerializer

from stats.models import Stat


class StatsViewSet(viewsets.ModelViewSet):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
    permission_classes = (AllowAny,)

    @action(methods=['GET'], detail=False)
    def most_used_device_name(self, request, *args, **kwargs):
        year = request.query_params.get('year')
        max_stat = Stat.objects.filter(year=year).order_by('-device_usage_rate')
        if not max_stat:
            return Response({'test': 'fail'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(max_stat[0], many=False)
        return Response({'result': serializer.data}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def most_used_year(self, request, *args, **kwargs):
        device_id = request.query_params.get('device_id')
        device = Device.objects.filter(device_id=device_id).first()
        if not device:
            return Response({'test': 'fail'}, status=status.HTTP_400_BAD_REQUEST)

        max_stat = Stat.objects.filter(device_name=device.device_name).order_by('-device_usage_rate')
        if not max_stat:
            return Response({'test': 'fail'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(max_stat[0], many=False)
        return Response({'result': serializer.data}, status=status.HTTP_200_OK)
