from setuptools import setup

options = {
  'name': 'crocus',
  'version': '0.1',
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
  'zip_safe': False  
}

setup(**options)