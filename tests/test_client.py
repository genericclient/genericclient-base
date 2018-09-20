import pytest
try:
    from unittest import mock
except ImportError:
    import mock

from genericclient_base import BaseGenericClient, BaseEndpoint, BaseResource, ParsedResponse


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


def test_endpoints(monkeypatch, mock):
    class PostResource(BaseResource):
        pk_name = 'slug'

    class PostEndpoint(BaseEndpoint):
        resource_class = PostResource

    response = ParsedResponse(
        status_code=200,
        data={
            'id': 1,
            'slug': 'cats-demand-longer-breaks',
            'headline': 'Cats Demand Longer Breaks, Cleaner Litter, Slower Mice',
        },
    )

    class Client(BaseGenericClient):
        endpoint_classes = {
            'posts': PostEndpoint,
        }

    client = Client(url='http://dummy.org')

    monkeypatch.setattr(client.endpoint_class, 'request', mock.MagicMock(return_value=response))

    post = client.posts.get(slug='cats-demand-longer-breaks')
    assert post.__class__ is PostResource

    monkeypatch.setattr(client.endpoint_class, 'request', mock.MagicMock())

    post.save()

    client.posts.request.assert_called_with(
        'put', 'http://dummy.org/posts/cats-demand-longer-breaks', json={
            'id': 1,
            'slug': 'cats-demand-longer-breaks',
            'headline': 'Cats Demand Longer Breaks, Cleaner Litter, Slower Mice',
        }
    )


