import pytest

try:
    from unittest import mock
except ImportError:
    import mock

from genericclient_base import AmbiguousComparison
from genericclient_base import BaseResource


# Create your tests here.
class TestResource:

    @mock.patch('genericclient_base.BaseEndpoint')
    def test_equality(self, BaseEndpoint):
        endpoint = BaseEndpoint()
        res1 = BaseResource(endpoint, id=1)
        res2 = BaseResource(endpoint, id=1)
        res3 = BaseResource(endpoint, id=3)
        res4 = BaseResource(endpoint, id=1, username='username')

        assert res1 == res2
        assert res3 != res2
        with pytest.raises(AmbiguousComparison):
            assert res4 == res1

    @mock.patch('genericclient_base.BaseEndpoint')
    def test_repr(self, BaseEndpoint):
        endpoint = BaseEndpoint()
        endpoint.name = 'users'
        res1 = BaseResource(endpoint, id=1)

        representation = repr(res1)
        assert representation == '<BaseResource `users` id: 1>'
