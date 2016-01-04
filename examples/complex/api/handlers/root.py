import json

async def root(req, res):
  data = {
    'resource': 'root',
    'path': '/'
  }
  res.write(json.dumps(data))
  await res.end()

