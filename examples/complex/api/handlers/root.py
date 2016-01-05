import json

async def root(req, res):
  data = {
    'resource': 'root',
    'path': '/',
    'method': req.method.lower()
  }
  res.write(json.dumps(data))
  await res.end()

