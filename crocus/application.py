import asyncio
from urllib.parse import urlparse, parse_qsl
from crocus.server import Server
from crocus.helpers import RouteDict, DynamicObject


class Application(object):
  def __init__(self, loop=asyncio.get_event_loop(), handlers=RouteDict(), middlewares=[], **kwargs):
    self.loop = loop
    self.handlers = handlers
    self.middlewares = middlewares
    self.config = DynamicObject()
    self.set_default_config()
    self.errors = []
    for item in kwargs:
      setattr(self.config, item, kwargs[item])
  
  def __repr__(self):
    params = (self.loop, self.handlers, self.middlewares, self.config)
    return '<Application(loop=%s, handlers=%s, middlewares=%s, config=%s)>' % params

  def set_default_config(self):
    self.config.default_encoding = 'utf8'
    self.config.debug = True

  def error(self, *args):
    [self.errors.append(item) for item in args]

  def use(self, *args):
    [self.middlewares.append(item) for item in args]

  def middleware(self, fn):
    self.use(fn)

  def add_handler(self, method, path, fn):
    self.handlers['%s:%s' % (method, path)] = fn
  
  def post(self, path, fn):
    self.add_handler('post', path, fn)

  def get(self, path, fn):
    self.add_handler('get', path, fn)

  def put(self, path, fn):
    self.add_handler('put', path, fn)

  def delete(self, path, fn):
    self.add_handler('delete', path, fn)

  def patch(self, path, fn):
    self.add_handler('patch', path, fn)

  def options(self, path, fn):
    self.add_handler('options', path, fn)

  def head(self, path, fn):
    self.add_handler('head', path, fn)

  def trace(self, path, fn):
    self.add_handler('trace', path, fn)

  def connect(self, path, fn):
    self.add_handler('connect', path, fn)
  
  def run(self, host='127.0.0.1', port=5000, **kwargs):
    debug = kwargs.get('debug', True)
    keep_alive = kwargs.get('keep_alive', 75)
    self.config.debug = debug
    self.config.host = host
    self.config.port = port
    self.config.debug = debug
    self.config.keep_alive = keep_alive
    server_input = {
      'debug': debug,
      'keep_alive': keep_alive,
      'handlers': self.handlers,
      'middlewares': self.middlewares,
      'config': self.config
    }
    f = self.loop.create_server(lambda: Server(**server_input), host, str(port))
    srv = self.loop.run_until_complete(f)
    print('==> Running on http://%s:%s' % (host, port))
    try:
      self.loop.run_forever()
    except KeyboardInterrupt:
      print('==> Stopped http://%s:%s' % (host, port))

