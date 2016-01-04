import aiohttp.server
from crocus.request import Request
from crocus.response import Response
from crocus.helpers import RouteDict, DynamicObject


class Server(aiohttp.server.ServerHttpProtocol):
  def __init__(self, *args, **kwargs):
    super(Server, self).__init__(*args, **kwargs)
    self.handlers = kwargs.get('handlers', RouteDict())
    self.middlewares = kwargs.get('middlewares', [])
    self.config = kwargs.get('config', DynamicObject())

  async def handle_request(self, message, payload):
    req_input = {
      'method': message.method,
      'path': message.path,
      'headers': message.headers,
      'encoding': self.config.default_encoding
    }
    body = await payload.read()
    if body:
      req_input['body'] = body
    request = Request(**req_input)
    await request.prepare()
    handler_key = '%s:%s' % (request.method.lower(), request.path)
    (handler, params) = self.handlers.get(handler_key)
    request.params = DynamicObject.from_dict(params)
    response = Response(
      self.writer, 200, http_version=message.version
    )
    response.encoding = self.config.default_encoding
    response.header('Content-Type', 'application/json')
    if handler:
      for item in self.middlewares:
        middleware = await item(request, response)
        if middleware == Response.FINISH_CODE:
          return
        await handler(request, response)
      return
    response.status = 404
    response.send_headers()
    not_found_params = (request.method.encode(self.config.default_encoding), request.path.encode(self.config.default_encoding))
    response.write('%s %s NOT FOUND' % not_found_params)
    await response.end()
    return

