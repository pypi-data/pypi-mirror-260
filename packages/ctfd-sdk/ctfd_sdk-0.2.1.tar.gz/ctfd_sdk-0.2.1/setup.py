# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ctfd_sdk']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.27.0,<0.28.0', 'python-dotenv>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'ctfd-sdk',
    'version': '0.2.1',
    'description': 'Python SDK for CTFd REST API',
    'long_description': '# CTFd SDK for Python\n\n## Setup\n\n```bash\npython -m venv env\nsource env/bin/activate\npoetry install\n```\n',
    'author': 'Simon Plhak',
    'author_email': 'plhak.s@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
