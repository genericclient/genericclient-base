import pytest
from genericclient_base.response import ParsedResponse


def test_endpoint_all(monkeypatch, patched_client):
    response = ParsedResponse(
        status_code=200,
        data=[{'id': 1}, {'id': 2}, {'id': 3}]
    )
    monkeypatch.setattr(patched_client.endpoint_class, 'request', lambda *args, **kwargs: response)
    users = patched_client.users.all()
    assert len(users) == 3


def test_endpoint_create(monkeypatch, patched_client):
    user = {'id': 1, 'username': 'user1'}
    response = ParsedResponse(
        status_code=201,
        data=user
    )
    monkeypatch.setattr(patched_client.endpoint_class, 'request', lambda *args, **kwargs: response)

    user_resource = patched_client.users.create(user)
    assert user_resource.id == 1
    assert user_resource.username == 'user1'


def test_endpoint_create_or_update(monkeypatch, patched_client):
    user = {'id': 1, 'username': 'user1'}
    response = ParsedResponse(
        status_code=200,
        data=user
    )
    monkeypatch.setattr(patched_client.endpoint_class, 'request', lambda *args, **kwargs: response)
    user_resource = patched_client.users.create_or_update(user)
    assert user_resource.id == 1
    assert user_resource.username == 'user1'


def test_endpoint_get_or_create(monkeypatch, patched_client):
    user = {'id': 1, 'username': 'user1'}
    response = ParsedResponse(
        status_code=200,
        data=user
    )
    monkeypatch.setattr(patched_client.endpoint_class, 'request', lambda *args, **kwargs: response)
    user_resource = patched_client.users.get_or_create(
        username='user1',
        defaults={'group': 'watchers'}
    )
    assert user_resource.id == 1
    assert user_resource.username == 'user1'


def test_endpoint_create_httperror(monkeypatch, patched_client):
    user = {
        'id': 1,
        'username': 'user1',
        'group': 'watchers',
    }

    response = ParsedResponse(
        status_code=500,
    )
    monkeypatch.setattr(patched_client.endpoint_class, 'request', lambda *args, **kwargs: response)

    with pytest.raises(patched_client.HTTPError):
        patched_client.users.create(user)

def test_endpoint_delete(monkeypatch, patched_client):
    response = ParsedResponse(
        status_code=204,
    )
    monkeypatch.setattr(patched_client.endpoint_class, 'request', lambda *args, **kwargs: response)
    patched_client.users.delete(1)


def test_endpoint_delete_404(monkeypatch, patched_client):
    response = ParsedResponse(
        status_code=404,
    )
    monkeypatch.setattr(patched_client.endpoint_class, 'request', lambda *args, **kwargs: response)
    with pytest.raises(patched_client.ResourceNotFound):
        patched_client.users.delete(1)


def test_endpoint_delete_httperror(monkeypatch, patched_client):
    response = ParsedResponse(
        status_code=500,
    )
    monkeypatch.setattr(patched_client.endpoint_class, 'request', lambda *args, **kwargs: response)
    with pytest.raises(patched_client.HTTPError):
        patched_client.users.delete(1)


def test_endpoint_filter(monkeypatch, patched_client):
    response = ParsedResponse(
        status_code=200,
        data=[{'id': 1}, {'id': 2}]
    )
    monkeypatch.setattr(patched_client.endpoint_class, 'request', lambda *args, **kwargs: response)
    users = patched_client.users.filter(group="watchers")
    assert len(users) == 2


def test_endpoint_get(monkeypatch, patched_client):
    response = ParsedResponse(
        status_code=200,
        data={'id': 1, 'username': 'user1'}
    )
    monkeypatch.setattr(patched_client.endpoint_class, 'request', lambda *args, **kwargs: response)
    user2 = patched_client.users.get(id=1)
    assert user2.username == 'user1'

    response = ParsedResponse(
        status_code=404,
    )
    monkeypatch.setattr(patched_client.endpoint_class, 'request', lambda *args, **kwargs: response)
    with pytest.raises(patched_client.ResourceNotFound):
        patched_client.users.get(id=9999)


def test_endpoint_links(monkeypatch, patched_client):
    response = ParsedResponse(
        status_code=200,
        data=[{'id': 2, 'username': 'user2'}],
        headers={'link': '<http://dummy.org/users?page=1>; rel=previous, <http://dummy.org/users?page=3>; rel=next'}
    )
    monkeypatch.setattr(patched_client.endpoint_class, 'request', lambda *args, **kwargs: response)
    users = patched_client.users.all()

    assert users.response.links == {
        'next': {'url': 'http://dummy.org/users?page=3', 'rel': 'next'},
        'previous': {'url': 'http://dummy.org/users?page=1', 'rel': 'previous'}
    }

