class BaseError(Exception):
  def __repr__(self):
    return '<BaseError>'



class HandlerTypeError(BaseError):
  def __init__(self, name):
    self.name = name
    self.message = 'Handler function "%s" should be a coroutine.' % self.name

  def __repr__(self):
    return '<HandlerTypeError(name=%s)>' % self.name

