from rest_framework import viewsets
from devices.models import Device
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from devices.serializers import DevicesSerializer
from stats.models import Stat
from core.common import device_name_map


class DevicesViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DevicesSerializer
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'devices': serializer.data}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def most_yearly(self, request, *args, **kwargs):
        stats_queryset = Stat.objects.all()
        devices = []
        for year in [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]:
            temp = {}
            max_stat = stats_queryset.filter(year=year).order_by('-device_usage_rate')
            if max_stat:
                temp['year'] = max_stat[0].year
                temp['device_name'] = device_name_map[max_stat[0].device_name]
                temp['rate'] = max_stat[0].device_usage_rate
                temp['device_id'] = Device.objects.get(device_name=max_stat[0].device_name).device_id
                devices.append(temp)

        return Response({'devices': devices}, status=status.HTTP_200_OK)
