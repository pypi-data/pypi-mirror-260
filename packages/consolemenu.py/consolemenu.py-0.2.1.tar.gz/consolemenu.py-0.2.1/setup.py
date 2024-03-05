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
    'version': '0.2.1',
    'description': "A simple Python console (terminal) menu that work's on any OS",
    'long_description': '## Usage\n```py\nimport consolemenu_py as cm\n\nasync def main():\n    # Create the main menu. The name should usually be the name of your program\n    mm = cm.MainMenu("Example Program")\n\n    # This will enter an empty sub-menu\n    mm.add_item(cm.Menu("A sub-menu!"))\n\n    # This will print "Hello World!" to the console\n    mm.add_item(cm.FunctionMenuItem("A function menu item", lambda _: print("Hello World!")))\n\n    # This will only return if the user exists the main menu\n    await mm.run()\n```\n\n## License\nThis package is licensed under MIT, see `LICENSE`',
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
