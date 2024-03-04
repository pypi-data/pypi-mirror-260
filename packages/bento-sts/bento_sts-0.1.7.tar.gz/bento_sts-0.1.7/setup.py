# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'swagger_server': 'src/swagger_server',
 'swagger_server.controllers': 'src/swagger_server/controllers',
 'swagger_server.models': 'src/swagger_server/models',
 'swagger_server.test': 'src/swagger_server/test'}

packages = \
['bento_sts',
 'bento_sts.api',
 'bento_sts.config_sts',
 'bento_sts.errors',
 'bento_sts.main',
 'bento_sts.query',
 'swagger_server',
 'swagger_server.controllers',
 'swagger_server.models',
 'swagger_server.test']

package_data = \
{'': ['*'],
 'bento_sts': ['static/*', 'templates/*', 'templates/errors/*'],
 'swagger_server': ['.swagger-codegen/*', 'swagger/*']}

install_requires = \
['Bootstrap-Flask>=1.5.2',
 'Flask-Moment>=0.5.2',
 'Flask-Paginate>=2021.10.29',
 'Flask-WTF>=0.14.3',
 'Jinja2>=2.11.3',
 'MarkupSafe>=1.1.1',
 'PyYAML>=5.4.1',
 'WTForms-Components>=0.10.5',
 'WTForms>=2.1',
 'Werkzeug>=1.0.1',
 'bento-meta>=0.0.32',
 'connexion>=2.6.0',
 'flask-testing>=0.8.1,<0.9.0',
 'guess-language-spirit>=0.5.3',
 'gunicorn>=20.1.0',
 'idna>=2.6',
 'importlib_resources>=5.4.0',
 'itsdangerous>=0.24',
 'neo4j>=4.1',
 'python-dateutil>=2.6.1',
 'python-dotenv>=0.15.0',
 'python-editor>=1.0.3',
 'pytz>=2017.2',
 'requests>=2.20.0',
 'six>=1.15.0',
 'swagger-ui-bundle>=0.0.9',
 'urllib3>=1.26.5',
 'visitor>=0.1.3']

setup_kwargs = {
    'name': 'bento-sts',
    'version': '0.1.7',
    'description': 'Bento Simple Terminology Server',
    'long_description': '# bento-sts\n\nSimple Terminology Service for [Bento MDB](https://github.com/CBIIT/bento-mdb).\n\nSee [bento-meta documentation] for an overview of the Metamodel\nDatabase. The STS provides a web-based UI and a RESTful API for\nbrowsing and accessing graph data models and associated controlled\nvocabulary.\n\n## Install\n\n    pip install bento-sts\n\n## Run\n\nIn the run directory, provide a `.env` file, with your appropriate\nvalues for the environment variables given the the example file\n[bento-sts.env.eg](./python/bento-sts.env.eg).\n\nFor testing:\n\n    flask --app "bento_sts.sts:create_app()" run\n\n## API Docs\n\n\n\n',
    'author': 'Mark Benson',
    'author_email': 'mark.benson@nih.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
