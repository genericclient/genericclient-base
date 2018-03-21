import attr

from .utils import parse_headers_link


@attr.s
class ParsedResponse(object):
    status_code = attr.ib(type=int)
    data = attr.ib(default=None)
    headers = attr.ib(default={})

    @property
    def links(self):
        return parse_headers_link(self.headers)
