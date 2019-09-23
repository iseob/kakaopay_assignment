import pytest
from model_mommy import mommy
from munch import Munch
from rest_framework import status
from core.common import device_name_map

from stats.models import Stat


class TestDevicesCreate:
    @pytest.mark.django_db
    def test_should_create_device(self, api_client):
        # Given : device_id, device_name 데이터
        device_id = 'DIV_11'
        device_name = 'desktop'
        data = {'device_id': device_id, 'device_name': device_name}

        # When : api를 호출해서 생성
        response = api_client.post(f'/api/devices', data=data)

        # Then : 성공적으로 device row 생성
        created_device = Munch(response.data)

        assert status.HTTP_201_CREATED == response.status_code
        assert created_device.device_id == device_id
        assert created_device.device_name == device_name

    @pytest.mark.django_db
    def test_should_fail_to_create_device_when_duplicate_device_id(self, api_client):
        # Given : device_id, device_name 데이터
        device_id = 'DIV_11'
        device_name = 'desktop'
        data = {'device_id': device_id, 'device_name': device_name}

        # When : 같은 device_id로 device 생성하는 api 두번 호출
        api_client.post(f'/api/devices', data=data)
        api_client.post(f'/api/devices', data=data)
        response = api_client.get(f'/api/devices')

        # Then : 한개의 데이터만 생성
        assert 1 == len(response.data['devices'])


# 인터넷 뱅킹 서비스 접속 기기 목록 출력하는 API
class TestDevicesList:
    @pytest.fixture(autouse=True)
    def setup_devices(self):
        self.devices_size = 10
        mommy.make('devices.Device', _quantity=self.devices_size)

    @pytest.mark.django_db
    def test_should_list_devices(self, api_client):
        # Given : 10개의 테스트 데이터

        # When : 해당 API 호출
        response = api_client.get(f'/api/devices')

        # Then : status_code가 200이어야하고, 데이터는 총 10개를 받아야함
        assert status.HTTP_200_OK == response.status_code
        assert self.devices_size == len(response.data['devices'])


# 각 년도별로 인터넷뱅킹을 가장 많이 이용하는 접속 기기 출력하는 API
class TestYearlyMostDevicesList:
    @pytest.fixture(autouse=True)
    def setup_devices(self):
        self.test_device_ids = {
            'phone': 'D_1',
            'desktop': 'D_2',
            'laptop': 'D_3',
            'etc': 'D_4',
            'pad': 'D_5'
        }
        for _type in ['phone', 'desktop', 'laptop', 'etc', 'pad']:
            mommy.make('devices.Device', device_id=self.test_device_ids[_type], device_name=_type)
        for _year in [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]:
            for _type in ['phone', 'desktop', 'laptop', 'etc', 'pad']:
                mommy.make('stats.Stat', year=_year, device_name=_type)

    @pytest.mark.django_db
    def test_should_list_most_devices_yearly(self, api_client):
        # Given

        # When : 해당 API 호출
        response = api_client.get(f'/api/devices/most_yearly')

        # Then : status_code가 200이어야하고, 각 연도별로 가장 많이 사용하는 접속 기기가 출력되어야함
        result = response.data['devices']
        assert status.HTTP_200_OK == response.status_code
        for idx, _year in enumerate([2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]):
            max_stat = Stat.objects.filter(year=_year).order_by('-device_usage_rate')[0]
            assert device_name_map[max_stat.device_name] == result[idx]['device_name']
            assert max_stat.device_usage_rate == result[idx]['rate']
            assert self.test_device_ids[max_stat.device_name] == result[idx]['device_id']
