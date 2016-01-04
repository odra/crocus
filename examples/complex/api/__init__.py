from crocus import Crocus
from . import handlers, middlewares, errors

app = Crocus()

#errors
app.error(errors.SomeError)

#root routes
app.get('/', handlers.root.root)

#users routes
app.post('/users', handlers.users.create)
app.get('/users', handlers.users.search)

#application middlewares
app.use(middlewares.bodyparser, middlewares.auth)