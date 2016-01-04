import json

async def create(req, res):
  data = {
    'resource': 'users',
    'path': '/users',
    'body': req.body
  }
  res.write(json.dumps(data))
  await res.end()


async def search(req, res):
  data = {
    'resource': 'users',
    'path': '/users'
  }
  res.write(json.dumps(data))
  await res.end()

