.. _introduction_ref_label:

############
Introduction
############

Basic usage:


.. code:: python

  from crocus import Crocus

  app = Crocus()

  async def response_middleware(req, res):
    res.header('content-type', 'application/json')


  async def request_middleware(req, res):
    req.some_value = 'custom value'


  async def search_products(req, res):
    data = {
      'total': 1,
      'data': [
        'name': 'redbull',
        'qty': 10
      ]
    }
    res.write(json.dumps(data))
    res.end()


  app.use(response_middleware, request_middleware)
  app.get('/products', search_products)


  if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)


Features
--------

- asycnio + aiohttp
- async request handling
- stream writing
- request/response middleware


Installation
------------

Install crocus by running:

  .. code:: bash

    pip install crocus

Contribute
----------

- Issue Tracker: https://github.com/goldark/crocus/issues
- Source Code: https://github.com/goldark/crocus

Support
-------

If you are having issues, please let us know.
We have a mailing list located at: python-crocus@google-groups.com

License
-------

The project is licensed under the MIT license.

