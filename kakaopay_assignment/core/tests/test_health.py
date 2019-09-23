from rest_framework import status


class TestHealth:
    def test_should_get_health_response(self, api_client):
        response = api_client.get(f'/health/')

        assert status.HTTP_200_OK == response.status_code
        assert 'live' == response.data['health']
