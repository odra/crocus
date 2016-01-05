from urllib.parse import urlparse, parse_qsl
from crocus.helpers import DynamicObject, Dict

default_content_type = 'application/octet-stream'


def set_default_content_type(mimetype):
  global _default_content_type
  _default_content_type = mimetype


class Request(DynamicObject):
  def __init__(self, **kwargs):
    self.method = kwargs.get('method')
    self.path = kwargs.get('path')
    self.headers = kwargs.get('headers', {})
    self.body = kwargs.get('body', None)
    self.query = kwargs.get('params', {})
    self.content_type = None
    self.params = kwargs.get('params', DynamicObject())
    self.encoding = kwargs.get('encoding', 'utf8')
    self.app = kwargs.get('app', DynamicObject())

  def __repr__(self):
    params = (self.method, self.path, self.params, self.headers, self.body)
    return '<Request(method=%s, path=%s, params=%s, headers=%s, body=%s)>' % params

  async def prepare(self):
    await self.parse_headers()
    await self.parse_path()
    await self.parse_body()

  async def parse_headers(self):
    self.headers = Dict({k:self.headers[k] for k in self.headers})
    self.content_type = self.headers.get('Content-Type', default_content_type)

  async def parse_path(self):
    qs = urlparse(self.path)
    self.path = qs.path
    self.query = {item[0]:item[1] for item in parse_qsl(qs.query)}

  async def parse_body(self):
    if self.body is not None:
      self.body = self.body.decode(self.encoding)
