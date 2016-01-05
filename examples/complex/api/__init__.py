import sys;sys.path.append('../../')
from crocus import Crocus
from . import handlers, middlewares

app = Crocus()

#root routes
app.all('/', handlers.root.root)

#users routes
app.post('/users', handlers.users.create)
app.get('/users', handlers.users.search)

#application middlewares
app.use(middlewares.bodyparser, middlewares.auth)