import pytest
import requests


class ApiClient:

    def __init__(self, base_address):
        self.base_address = base_address

    def get(self, path="", params=None, headers=None):
        url = "{base_address}{path}".format(base_address=self.base_address, path=path)
        return requests.get(url=url, params=params, headers=headers)


@pytest.fixture
def regions_api():
    return ApiClient(base_address="https://regions-test.2gis.com/1.0/regions")
