from crocus.helpers import BaseError


class SomeError(BaseError):
  def __init__(self):
    super(SomeError, self).__init__()
    self.status = 403
    self.data = {
      'error': 'some random error'
    }

