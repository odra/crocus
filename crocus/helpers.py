import json
import collections
import re


class DynamicObject(object):
  def __init__(self, *args, **kwargs):
    if len(args) > 0 and isinstance(args[0], dict):
      for item in args[0]:
        setattr(self, item, args[0][item])
    for item in kwargs:
      setattr(self, item, kwargs[item])

  def __repr__(self):
    return '<DynamicObject>'

  @staticmethod
  def from_json(raw):
    data = json.loads(raw)
    return DynamicObject.from_dict(**data)

  @staticmethod
  def from_dict(data={}):
    return DynamicObject(**data)

  def __setattr__(self, name, value):
    if self.__dict__.get(name):
      super(DynamicObject, self).__setattr__(name, value)
    else:
      self.__dict__[name] = value

  def __getattr__(self, name):
    return None
  
  def __getattribute__(self, name):
    return super(DynamicObject, self).__getattribute__(name)


class Dict(collections.MutableMapping):
  def __init__(self, *args, **kwargs):
    self.data = {}
    self.update(dict(*args, **kwargs))

  def __repr__(self):
    return '<Headers(%s)>' % self.data

  def __getitem__(self, key):
    for item in self.data:
      if item.lower() == key.lower():
        return self.data[item] 
    return None

  def __setitem__(self, key, value):
    self.data[key] = value

  def __delitem__(self, key):
    if self.get(key) is None:
      return
    del self.data[key]

  def __iter__(self):
    return iter(self.data)

  def __len__(self):
    return len(self.data)


class RouteDict(Dict):
  def __repr__(self):
    return '<RouteDict(%s)>' % self.data

  def __getitem__(self, key):
    method = key.split(':')[0]
    path = key.replace('%s:' % method, '')
    route = self.data.get(path)
    if route and method in route['methods']:
      return (self.data[path]['methods'][method], {})
    match = None
    for item in self.data:
      match = re.match('^%s$' % self.data[item]['regex'], path)
      if match and method in self.data[item]['methods']:
        route = self.data[item]
        break
    if match is None:
      return (None, None)
    return (route['methods'][method], dict(zip(route['params'], match.groups())))

  def __setitem__(self, key, value):
    method = key.split(':')[0]
    path = key.replace('%s:' % method, '')
    if not path in self.data:
      self.data[path] = {
        'methods': {},
        'regex': self.parse_path(path),
        'params': [item.replace(':', '') for item in path.split('/') if item.startswith(':')]
      }
    if not method in self.data[path]['methods']:
      self.data[path]['methods'][method] = value

  def parse_path(self, path):
    output = ['']
    splited_path = path.split('/')
    for item in splited_path:
      if not item:
        continue
      if item.startswith(':'):
        output.append('(.*)')
      else:
        output.append(item)
    if len(output) == 1:
      return '/'
    return '/'.join(output)

