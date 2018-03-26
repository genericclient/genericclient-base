import pytest

from genericclient_base import exceptions, utils


def test_urljoin():
    url = utils.urljoin(
        'http://example.com',
        ['users', 2],
        trail=True
    )
    assert url == 'http://example.com/users/2/'

    url = utils.urljoin(
        'http://example.com',
        ['users', 2],
        trail=False
    )
    assert url == 'http://example.com/users/2'

    url = utils.urljoin(
        'http://example.com/',
        ['users', 2],
        trail=True
    )
    assert url == 'http://example.com/users/2/'

    url = utils.urljoin(
        'http://example.com/users',
        [2, 'notify'],
        trail=True
    )
    assert url == 'http://example.com/users/2/notify/'


def test_find_pk():
    payload = {
        'id': 1
    }

    assert utils.find_pk(payload) == 1

    payload = {
        'id': 1,
        'slug': '12-ways-to-clickbait'
    }

    assert utils.find_pk(payload) == 1

    payload = {
        'slug': '12-ways-to-clickbait'
    }

    assert utils.find_pk(payload) == '12-ways-to-clickbait'

    payload = {
        'id': 1,
        'username': 'user1'
    }

    assert utils.find_pk(payload) == 1

    payload = {
        'username': 'user1'
    }

    assert utils.find_pk(payload) == 'user1'

    payload = {
        'name': 'user 1'
    }

    with pytest.raises(exceptions.UnknownPK):
        utils.find_pk(payload)


def test_parse_link():
    headers = {
        'Link': '<http:/localhost/front.jpeg>; rel=front',
    }
    assert utils.parse_headers_link(headers) == {'front': {'rel': 'front', 'url': 'http:/localhost/front.jpeg'}}

    headers = {
        'Link': '<http:/localhost/front.jpeg>',
    }
    assert utils.parse_headers_link(headers) == {'http:/localhost/front.jpeg': {'url': 'http:/localhost/front.jpeg'}}

    headers = {}
    assert utils.parse_headers_link(headers) == {}

    headers = {
        'Link': '""',
    }
    assert utils.parse_headers_link(headers) == {}
