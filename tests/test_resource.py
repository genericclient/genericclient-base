import pytest

try:
    from unittest import mock
except ImportError:
    import mock

from genericclient_base import AmbiguousComparison
from genericclient_base import BaseResource


@mock.patch('genericclient_base.BaseEndpoint')
def test_equality(BaseEndpoint):
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
def test_repr(BaseEndpoint):
    endpoint = BaseEndpoint()
    endpoint.name = 'users'
    res1 = BaseResource(endpoint, id=1)

    representation = repr(res1)
    assert representation == '<BaseResource `users` id: 1>'


@mock.patch('genericclient_base.BaseEndpoint')
def test_attributes(BaseEndpoint):
    endpoint = BaseEndpoint()
    user = BaseResource(endpoint, id=1, username='user')
    assert user.pk == 1
    assert user.username == 'user'
    user.username = 'user1'
    assert user.payload['username'] == 'user1'

    with pytest.raises(AttributeError):
        user.group

    user = BaseResource(endpoint, username='user')
    assert user.pk is None

    user = BaseResource(endpoint, uuid='123abc', username='user')
    assert user.pk == '123abc'


@mock.patch('genericclient_base.BaseEndpoint')
def test_set_fk(BaseEndpoint):
    endpoint = BaseEndpoint()
    endpoint2 = BaseEndpoint()
    user = BaseResource(endpoint, id=1)
    group = BaseResource(endpoint2, id=2)
    user.group = group
    assert user.payload['group'] == 2


@mock.patch('genericclient_base.BaseEndpoint')
def test_protocol(BaseEndpoint):
    endpoint = BaseEndpoint()
    user = BaseResource(endpoint, id=1)

    with pytest.raises(NotImplementedError):
        user.save()

    with pytest.raises(NotImplementedError):
        user.delete()
