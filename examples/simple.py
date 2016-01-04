from crocus import Crocus

app = Crocus()

@app.get('/')
async def hello(req, res):
  res.code = 200
  res.header('content-type', 'text/plain')
  res.write(b'chunk data')
  await res.end(b'another chunk data')


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000)

