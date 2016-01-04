import json
from api import errors

async def root(req, res):
  raise errors.SomeError()
  data = {
    'resource': 'root',
    'path': '/'
  }
  res.write(json.dumps(data))
  await res.end()

