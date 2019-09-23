import pytest
from devices.models import Device


class TestDevicesCreate:
    @pytest.mark.django_db
    def test_should_import_devoce_data(self, api_client):
        # Given : Sample Data
        expected_device_count = 5

        # When : 해당 데이터를 database에 넣는 코드 실행
        Device.load_initial_data()

        # Then : 총 5개의 데이터가 들어가야함
        devices = Device.objects.all()
        assert expected_device_count == len(devices)

