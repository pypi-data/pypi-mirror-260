# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['consolemenu_py']

package_data = \
{'': ['*']}

install_requires = \
['aioconsole>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'consolemenu.py',
    'version': '0.1.0',
    'description': "A simple Python console (terminal) menu that work's on any OS",
    'long_description': None,
    'author': 'Pirulax',
    'author_email': 'patrikjankovics7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
