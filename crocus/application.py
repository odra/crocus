import asyncio
import inspect
from crocus.server import Server
from crocus.helpers import RouteDict, DynamicObject
from crocus import errors
import logging

methods = ('post', 'get', 'put', 'delete', 'patch', 'options', 'head', 'trace', 'connect')


class Application(object):
  def __init__(self, loop=asyncio.get_event_loop(), handlers=RouteDict(), middlewares=[], **kwargs):
    self.loop = loop
    self.handlers = handlers
    self.middlewares = middlewares
    self.config = DynamicObject()
    self.set_default_config()
    for item in kwargs:
      setattr(self.config, item, kwargs[item])
  
  def __repr__(self):
    params = (self.loop, self.handlers, self.middlewares, self.config)
    return '<Application(loop=%s, handlers=%s, middlewares=%s, config=%s)>' % params

  def set_default_config(self):
    self.config.default_encoding = 'utf8'
    self.config.keep_alive = '75'
    self.config.debug = True
    self.config.default_status = 200
    self.config.logger = logging.getLogger(__name__)
    level = logging.DEBUG
    if self.config.debug is False:
      level = logging.INFO
    self.config.logger.setLevel(level)
    logging.basicConfig(format='%(levelname)s:%(message)s', level=level)

  def use(self, *args):
    [self.middlewares.append(item) for item in args]

  def add_handler(self, method, path, fn):
    if inspect.iscoroutinefunction(fn) is False:
      self.config.logger.error('Hanlder %s should be a coroutine.' % fn.__name__)
      raise errors.HandlerTypeError(fn.__name__)
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
  
  def all(self, path, fn):
    [getattr(self, method)(path, fn) for method in methods]
  
  def run(self, host='127.0.0.1', port=5000, **kwargs):
    self.config.host = host
    self.config.port = port
    server_input = {
      'debug': self.config.debug,
      'keep_alive': self.config.keep_alive,
      'handlers': self.handlers,
      'middlewares': self.middlewares,
      'config': self.config
    }
    f = self.loop.create_server(lambda: Server(**server_input), host, str(port))
    srv = self.loop.run_until_complete(f)
    self.config.logger.info('Running on http://%s:%s' % (host, port))  
    try:
      self.loop.run_forever()
    except KeyboardInterrupt:
      self.config.logger.info('Stopped http://%s:%s' % (host, port))

