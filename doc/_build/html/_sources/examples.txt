.. _examples_ref_label:

########
Examples
########


For complex examples see: https://www.github.com/goldark/crocus/examples

*********
Simpliest
*********

.. code:: python

  from crocus import Crocus

  app = Crocus()

  async def handler(req, res):
    res.write('chunk\n')
    res.write('another chunk\n')
    res.end()

  app.get(handler)

  if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)


***********************
Request body middleware
***********************

.. code:: python

  async def json_body(req, res):
    if req.body is None:
      return
    try:
      req.body = json.loads(req.body)
    except json.decoder.JSONDecodeError:
      data = {
        'error': 'invalid json'
      }
      res.status = 400
      res.write(json.dumps(data))
      res.end()
      return res.finish()

  app.use(json_body)

*************************
Authentication middleware
*************************

.. code:: python

  async def auth(req, res):
    if req.header('x-api-token') is None:
      data = {
        'error': 'unauthorized'
      }
      res.status = 401
      res.write(json.dumps(data))
      res.end()
      return res.finish()

  app.use(auth)

*******************
Response middleware
*******************

.. code:: python

  async def response_middleware(req, res):
    res.header('content-type', 'application/json')

  app.use(response_middleware)

*********************
Application variables
*********************

.. code:: python

  from crocus import Crocus
  import pymongo
  import redis as r

  redis = r.StrictRedis()
  mongo = pymongo.MongoClient()

  app = Crocus(redis=redis, mongo=mongo)

  print(app.config.redis) # can be used anywhere
  print(app.config.mongo) #can be used anywhere


