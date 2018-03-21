from unittest import TestCase

from genericclient_base import utils


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
