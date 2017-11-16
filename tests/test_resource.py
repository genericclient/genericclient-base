from unittest import TestCase

try:
    from unittest import mock
except ImportError:
    import mock

from genericclient_base import AmbiguousComparison
from genericclient_base import BaseResource


# Create your tests here.
class ResourceTestCase(TestCase):

    @mock.patch('genericclient_base.BaseEndpoint')
    def test_equality(self, BaseEndpoint):
        endpoint = BaseEndpoint()
        res1 = BaseResource(endpoint, id=1)
        res2 = BaseResource(endpoint, id=1)
        res3 = BaseResource(endpoint, id=3)
        res4 = BaseResource(endpoint, id=1, username='username')

        self.assertEqual(res1, res2)
        self.assertNotEqual(res3, res2)
        with self.assertRaises(AmbiguousComparison):
            res4 == res1

    @mock.patch('genericclient_base.BaseEndpoint')
    def test_repr(self, BaseEndpoint):
        endpoint = BaseEndpoint()
        endpoint.name = 'users'
        res1 = BaseResource(endpoint, id=1)

        representation = repr(res1)
        self.assertEqual(representation, '<BaseResource `users` id: 1>')
