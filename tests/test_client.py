import pytest
try:
    from unittest import mock
except ImportError:
    import mock

from genericclient_base import BaseGenericClient, BaseEndpoint


def test_host():
    client = BaseGenericClient(url='http://dummy.org')
    assert client.host == 'dummy.org'

    client = BaseGenericClient(url='http://dummy.org:8000')
    assert client.host == 'dummy.org:8000'

    client = BaseGenericClient(url='http://dummy.org:8000/api')
    assert client.host == 'dummy.org:8000'

    client = BaseGenericClient(url='http://dummy.org/api')
    assert client.host == 'dummy.org'


def test_protocol(monkeypatch, client, response):
    with pytest.raises(NotImplementedError):
        client.hydrate_data(response)

    with pytest.raises(NotImplementedError):
        client.make_session()

    monkeypatch.setattr(client, 'make_session', mock.MagicMock())

    session = client.session
    assert session is not None


def test_attribute(client):
    endpoint = client.users
    assert isinstance(endpoint, BaseEndpoint)
