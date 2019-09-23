import pytest
from model_mommy import mommy


# 연도별로 가장 많이 접속한 기기 이름
class TestMostAccessedDeivceYearFromYear:
    @pytest.fixture(autouse=True)
    def setup_devices(self):
        self.top_device_rate = 95.1
        self.other_device_rate = 94.9
        for _type in ['phone', 'desktop', 'laptop', 'etc', 'pad']:
            if _type == 'desktop':
                mommy.make('stats.Stat', year=2011, total_usage_rate=50.0, device_name=_type,
                           device_usage_rate=self.top_device_rate)
            else:
                mommy.make('stats.Stat', year=2011, total_usage_rate=50.0, device_name=_type,
                           device_usage_rate=self.other_device_rate)
        test_device_id = 'DIV_11'
        test_device_name = 'desktop'
        self.test_device = mommy.make('devices.Device', device_id=test_device_id, device_name=test_device_name)

    @pytest.mark.django_db
    def test_should_get_most_accessed_device_name_from_year(self, api_client):
        # Given : Year
        test_year = 2011
        expected_device_name = '데스크탑 컴퓨터'
        expected_device_rate = self.top_device_rate

        # When : 해당 API 호출
        response = api_client.get(f'/api/stats/most_used_device_name?year={test_year}')

        # Then : 가장 많이 접속하는 기기 데스크탑 컴퓨터, 95.1 출력
        result = response.data['result']
        assert 200 == response.status_code
        assert expected_device_name == result['device_name']
        assert expected_device_rate == result['rate']


# 디바이스 아이디를 입력받아 인터넷 뱅킹에 접속 비율이 가장 많은 해를 출력하는 API
class TestMostAccessedYearFromDeviceId:
    @pytest.fixture(autouse=True)
    def setup_devices(self):
        self.top_device_rate = 95.1
        self.other_device_rate = 94.9
        self.most_accessed_year = 2017
        for _year in [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]:
            for _type in ['phone', 'desktop', 'laptop', 'etc', 'pad']:
                if _type == 'desktop' and _year == self.most_accessed_year:
                    mommy.make('stats.Stat', year=_year, total_usage_rate=50.0, device_name=_type,
                               device_usage_rate=self.top_device_rate)
                else:
                    mommy.make('stats.Stat', year=_year, total_usage_rate=50.0, device_name=_type,
                               device_usage_rate=self.other_device_rate)
        self.test_device_id = 'DIV_11'
        self.test_device_name = 'desktop'
        self.test_device = mommy.make('devices.Device', device_id=self.test_device_id,
                                      device_name=self.test_device_name)

    @pytest.mark.django_db
    def test_should_get_most_accessed_year_from_device_id(self, api_client):
        # Given : device_id, expected value
        expected_year = self.most_accessed_year
        expected_device_rate = self.top_device_rate
        expected_device_name = '데스크탑 컴퓨터'

        # When : 해당 API 호출
        response = api_client.get(f'/api/stats/most_used_year?device_id={self.test_device_id}')

        # Then : 접속 비율이 가장 많은 해 2017, desktop 출력
        result = response.data['result']
        assert 200 == response.status_code
        assert expected_year == result['year']
        assert expected_device_name == result['device_name']
        assert expected_device_rate == result['rate']

    @pytest.mark.django_db
    def test_should_fail_to_get_most_accessed_year_from_wrong_device_id(self, api_client):
        # Given : wrong_device_id
        wrong_device_id = 'wrong'

        # When : 해당 API 호출
        response = api_client.get(f'/api/stats/most_used_year?device_id={wrong_device_id}')

        # Then : 접속 비율이 가장 많은 해 2017, desktop 출력
        assert 400 == response.status_code
