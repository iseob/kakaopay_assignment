import pytest
from pytest_django.lazy_django import skip_if_no_django


@pytest.fixture()
def api_client():
    skip_if_no_django()

    from rest_framework.test import APIClient

    return APIClient()
