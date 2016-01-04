from setuptools import setup

options = {
  'name': 'crocus',
  'version': '0.2.2',
  'description': 'Python async http framework with asyncio + aiohttp (requires 3.5+)',
  'url': 'https://github.com/goldark/crocus',
  'author': 'Leonardo Rossetti',
  'author_email': 'leonardo@goldark.com.br',
  'license': 'MIT',
  'packages': ['crocus'],
  'install_requires': [
    'aiohttp==0.20.1',
    'chardet==2.3.0'
  ],
  'keywords': ['async', 'http', 'server', 'web framework', 'async http', 'asyncio'],
  'classifiers':[
    'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    'Topic :: Software Development :: Libraries :: Application Frameworks'
  ],
  'zip_safe': False 
}

setup(**options)