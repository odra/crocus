import json

async def bodyparser(req, res):
  content_type = req.content_type
  if content_type == 'application/json':
    try:
      req.body = json.loads(req.body)
    except json.decoder.JSONDecodeError:
      data = {
        'error': 'invalid json'
      }
      res.status = 400
      res.write(json.dumps(data))
      await res.end()
      return res.finish()


async def auth(req, res):
  if req.headers['x-api-token'] is None:
    data = {
      'error': 'unauthorized'
    }
    res.status = 401
    res.write(json.dumps(data))
    await res.end()
    return res.finish()

