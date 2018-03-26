from genericclient_base import BaseResourceSet


def test_resource_set(response):
    resource_set = BaseResourceSet(response, [1, 2, 3])
    assert len(resource_set) == 3
