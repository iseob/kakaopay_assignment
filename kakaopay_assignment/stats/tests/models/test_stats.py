import pytest
from stats.models import Stat


class TestStatsCreate:
    @pytest.mark.django_db
    def test_should_import_sample_data(self, api_client):
        # Given : Sample Data
        expected_device_count = 37

        # When : 해당 데이터를 database에 넣는 코드 실행
        Stat.load_initial_data()

        # Then : 총 37개의 데이터가 들어가야함
        stats = Stat.objects.all()
        assert expected_device_count == len(stats)

