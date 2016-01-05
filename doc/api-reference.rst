.. _api_reference_ref_label:

#############
API Reference
#############

***********
Application
***********

.. currentmodule:: crocus.application

.. class:: Application(loop=asyncio.get_event_loop(), handlers=RouteDict(), middlewares=[], **kwargs) 

  .. attribute:: loop

    evento loop to be used

  .. attribute:: handlers

    Used to store route handlers.

  .. attribute:: middlewares

    Stores application middlewares.

  .. attribute:: config

    All values used in **kwargs will be stored in this property.

    Usefull to store session keys, database objects, etc.

  .. function:: add_handler(method, path, fn)
    
    Adds a handler for a given http method and path.

  .. function:: use(*args)

    Adds async function(s) handlers as a middleware.

  .. function:: post(path, fn)

    Adds a post handler for a given path.

  .. function:: get(path, fn)

    Adds a get handler for a given path.

  .. function:: put(path, fn)

    Adds a put handler for a given path.

  .. function:: delete(path, fn)

    Adds a delete handler for a given path.

  .. function:: patch(path, fn)

    Adds a patch handler for a given path.

  .. function:: head(path, fn)

    Adds a head handler for a given path.

  .. function:: options(path, fn)

    Adds a options handler for a given path.

  .. function:: trace(path, fn)

    Adds a trace handler for a given path.

  .. function:: connect(path, fn)

    Adds a connect handler for a given path.

  .. function:: all(path, fn)

    Adds a handler for all http methods whithin given path.
  
  .. function:: run(host='127.0.0.1', port=5000)

    Runs the application in a given host and port.


********
Handlers
********

Every request handler is a python async function which uses two arguments: a request and a response.

.. code:: python

  async def handler(req, res):
    data = await some_action(req.data)
    res.status = 201 #default is 200
    res.write(json.dumps(data))
    await res.end()

***********
Middlewares
***********

Middlewares use the same async functions as handlers, but they are executed before the handler itself.

Middlewares are useful for changing or validating request data.You can also end a request in a middleware before it reaches the designated handler, in this case the middleware functions needs to return the "finish" method from the response object (otherwise the request will go on).

.. code:: python

  async def bodyparser(req, res):
    try:
      req.body = json.loads(req.body)
    except except json.decoder.JSONDecodeError:
      res.status = 400
      res.write(json.dumps({'error': 'invalid json'}))
      await res.end()
      return res.finish() #mandatory if middleware needs to end the current request

*******
Request
*******

.. currentmodule:: crocus.request

.. class:: Request(method=None, path=None, headers={}, body=None, params={}, content_type=None, params=DynamicObject())

  .. attribute:: method

    request http method

  .. attribute:: path

    http request path (without query string)

  .. attribute:: headers

    http request headers in key:value format, it is not case sensitive whilte retrieving a header.

  .. attribute:: query
    
    url query string in a key:value (dict) format.

  .. attribute:: body

    request content body

  .. attribute:: content_type

    request body content-type (if any). default is application/octet-stream

  .. attribute:: params

    DynamicObject that stores dyanmic url parameters.

  .. attribute:: app

    A DynamicObject which stores the application config data

  .. function:: prepare()

    async method that prepares the request (parse headers, path, body, etc)

  .. function:: parse_headers()

    parses the http headers (called by prepare)

  .. function:: parse_path()

    parses the request path (route params, query string, etc)

********
Response
********

.. currentmodule:: crocus.response

.. class:: Response()

  .. attribute:: status

    response http status code

  .. function:: header(key, value=None, defaults=None)

    HTTP response reader manipultion.

    If only key is provided it return its value (returns the default value is not found).

    It sets a header value if provided with a key and value.

  .. function:: write(chunk)

    writes a response content chunk

  .. function:: end(chunk=None)

    ends the request stream (option chunk can be provided).

  .. function:: finish()

    returns a finish code to notify the application that the middleware should end the request 

******
Server
******

.. currentmodule:: crocus.helpers

.. class:: Server(handlers=RouteDict(), middlewares={}, config=DynamicObject())

  Implementation of aiohttp.server.ServerHttpProtocol to handle event loop requests.

  Config stores the application config data to be used in every request handler.

*******
Helpers
*******

.. currentmodule:: crocus.helpers

.. class:: DynamicObject(**kwargs)

  An object that can store any property, returns None if the property does not exist.

  .. function:: from_json(data)

    creates a instance object from a json string

  .. function:: from_dict(data):

    creates an instance object from a dictionary

.. class:: Dict()
  
  A dictionary (collections.MutableMapping) used to store headers. It is case insensitive when retrieving values.

.. class:: RouteDict()

  Implementation of collections.MutableMapping it stores the server routes and handlers.
