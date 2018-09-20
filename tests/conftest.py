try:
    from unittest import mock as _mock
except ImportError:
    import mock as _mock
import pytest

from genericclient_base import BaseGenericClient
from genericclient_base.response import ParsedResponse


@pytest.fixture
def response():
    return ParsedResponse(
        status_code=200,
        data='ok',
    )


@pytest.fixture
def mock():
    return _mock


@pytest.fixture
def client():
    return BaseGenericClient(url='http://dummy.org')


@pytest.fixture
def patched_client(monkeypatch, mock, client, response):
    monkeypatch.setattr(client, 'make_session', mock.MagicMock())
    monkeypatch.setattr(client.endpoint_class, 'request', response)
    return client
