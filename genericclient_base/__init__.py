try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from . import exceptions, utils
from .routes import DetailRoute, ListRoute

_version = "0.0.4"
__version__ = VERSION = tuple(map(int, _version.split('.')))


AmbiguousComparison = exceptions.AmbiguousComparison
MultipleResourcesFound = exceptions.MultipleResourcesFound
ResourceNotFound = exceptions.ResourceNotFound
HTTPError = exceptions.HTTPError
NotAuthenticatedError = exceptions.NotAuthenticatedError
BadRequestError = exceptions.BadRequestError
UnknownPK = exceptions.UnknownPK


class BaseResource(object):
    whitelist = (
        '__class__',
        '_endpoint',
        'payload',
        'response',
        'save',
        'delete',
        '_urljoin',
    )

    def __init__(self, endpoint, response=None, **kwargs):
        self._endpoint = endpoint
        self.payload = kwargs
        self.response = response

        super(BaseResource, self).__init__()

    def __setattr__(self, name, value):
        if name == 'whitelist' or name in self.whitelist:
            return super(BaseResource, self).__setattr__(name, value)
        if isinstance(value, self.__class__) and hasattr(value, 'pk'):
            value = value.pk
        self.payload[name] = value

    def __getattr__(self, name):
        if name not in self.payload:
            raise AttributeError("{} on endpoint `{}` has not attribute '{}'".format(
                self.__class__.__name__,
                self._endpoint.name,
                name,
            ))
        return self.payload[name]

    def __repr__(self):
        return '<{0} `{1}` {2}: {3}>'.format(
            self.__class__.__name__, self._endpoint.name, self.pk_name, self.pk,
        )

    def __eq__(self, other):
        if self.payload != other.payload and self.pk == other.pk:
            raise AmbiguousComparison(
                "Payloads are different, but {}:{} is the same.".format(
                    self.pk_name, self.pk
                )
            )
        return self.payload == other.payload

    @property
    def pk_name(self):
        pk_name = None
        if 'id' in self.payload:
            pk_name = 'id'
        elif 'uuid' in self.payload:
            pk_name = 'uuid'
        return pk_name

    @property
    def pk(self):
        if self.pk_name is not None:
            return self.payload.get(self.pk_name)
        return None

    def _urljoin(self, *parts):
        return utils.urljoin(self._endpoint.url, parts, self._endpoint.trail)

    def save(self):
        raise not NotImplementedError

    def delete(self):
        raise not NotImplementedError


class BaseResourceSet(list):
    def __init__(self, response, items):
        self.response = response
        super(BaseResourceSet, self).__init__(items)


class BaseEndpoint(object):
    resource_set_class = BaseResourceSet
    resource_class = BaseResource
    detail_route_class = DetailRoute
    list_route_class = ListRoute

    def __init__(self, api, name):
        self.api = api
        self.name = name
        self.trail = self.api.trailing_slash
        self.url = utils.urljoin(self.api.url, [name], self.trail)

        super(BaseEndpoint, self).__init__()

    def __call__(self, _method='post', **kwargs):
        if kwargs:
            return self.detail_route_class(self, _method, **kwargs)
        else:
            return self.list_route_class(self, _method)

    def __repr__(self):
        return "<{} `{}`>".format(self.__class__.__name__, self.url)

    def _urljoin(self, *parts):
        return utils.urljoin(self.url, parts, self.trail)

    def status_code(self, response):
        return response.status_code

    def filter(self, **kwargs):
        response = self.request('get', self.url, params=kwargs)
        results = self.api.hydrate_json(response)
        return self.resource_set_class(response, [self.resource_class(self, **result) for result in results])

    def all(self):
        return self.filter()

    def get(self, **kwargs):
        try:
            pk = utils.find_pk(kwargs)
            url = self._urljoin(pk)
            response = self.request('get', url)
        except exceptions.UnknownPK:
            url = self.url
            response = self.request('get', url, params=kwargs)

        if self.status_code(response) == 404:
            raise exceptions.ResourceNotFound("No `{}` found for {}".format(self.name, kwargs))

        result = self.api.hydrate_json(response)

        if isinstance(result, list):
            if len(result) == 0:
                raise exceptions.ResourceNotFound("No `{}` found for {}".format(self.name, kwargs))
            if len(result) > 1:
                raise exceptions.MultipleResourcesFound("Found {} `{}` for {}".format(len(result), self.name, kwargs))

            return self.resource_class(self, response, **result[0])

        return self.resource_class(self, response, **result)

    def create(self, payload):
        response = self.request('post', self.url, json=payload)
        if self.status_code(response) != 201:
            raise exceptions.HTTPError(response)

        result = self.api.hydrate_json(response)
        return self.resource_class(self, response, **result)

    def get_or_create(self, **kwargs):
        defaults = kwargs.pop('defaults', {})
        try:
            resource = self.get(**kwargs)
            return resource
        except exceptions.ResourceNotFound:
            params = {k: v for k, v in kwargs.items()}
            params.update(defaults)
            return self.create(params)

    def create_or_update(self, payload):
        if 'id' in payload or 'uuid' in payload:
            return self.resource_class(self, response=None, **payload).save()

        return self.create(payload)

    def delete(self, pk):
        url = self._urljoin(pk)

        response = self.request('delete', url)

        if self.status_code(response) == 404:
            raise exceptions.ResourceNotFound("No `{}` found for pk {}".format(self.name, pk))

        if self.status_code(response) != 204:
            raise exceptions.HTTPError(response)

        return None

    def request(self, method, url, *args, **kwargs):
        raise NotImplementedError


class BaseGenericClient(object):
    endpoint_class = BaseEndpoint

    MultipleResourcesFound = MultipleResourcesFound
    ResourceNotFound = ResourceNotFound
    HTTPError = HTTPError
    NotAuthenticatedError = NotAuthenticatedError
    BadRequestError = BadRequestError
    UnknownPK = UnknownPK

    def __init__(self, url, auth=None, session=None, trailing_slash=False):
        self.session = self.set_session(session, auth)
        if not url.endswith('/'):
            url = '{}/'.format(url)
        self.url = url
        self.trailing_slash = trailing_slash
        super(BaseGenericClient, self).__init__()

    def set_session(self, session, auth):
        raise NotImplementedError

    def hydrate_json(self, response):
        raise NotImplementedError

    @property
    def host(self):
        scheme, netloc, path, _, query, _ = urlparse(
            self.url,
        )
        return netloc

    def __getattr__(self, name):
        return self.endpoint_class(self, name)
