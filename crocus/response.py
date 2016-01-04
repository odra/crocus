import aiohttp


class Response(aiohttp.Response):
  FINISH_CODE = 11031984

  def __repr__(self):
    params = (self.status, self.headers)
    return '<Response(status=%s, headers=%s)>' % params

  @property
  def status(self):
      return self._status
  
  @status.setter
  def status(self, value):
    self._reason = self.calc_reason(value)
    self._status = value

  def header(self, key, value=None, defaults=None):
    if value is None:
      return self.headers.get(key, defaults)
    self.headers[key] = value

  def write(self, chunk):
    if self.headers_sent is False:
      self.send_headers()
    try:
      _chunk = bytes(chunk.encode(self.encoding))
    except AttributeError:
      _chunk = chunk
    return super(Response, self).write(_chunk)

  async def end(self, chunk=None):
    if chunk:
      self.write(chunk)
    await self.write_eof()

  def finish(self):
    return Response.FINISH_CODE

