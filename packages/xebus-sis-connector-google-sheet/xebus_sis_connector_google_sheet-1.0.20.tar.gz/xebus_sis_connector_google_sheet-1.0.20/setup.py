# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['majormode',
 'majormode.xebus',
 'majormode.xebus.sis',
 'majormode.xebus.sis.connector',
 'majormode.xebus.sis.connector.google_sheet']

package_data = \
{'': ['*']}

install_requires = \
['gspread>=6.0,<7.0',
 'perseus-core-library>=1.19,<2.0',
 'perseus-getenv-library>=1.0,<2.0',
 'requests>=2.31,<3.0',
 'unidecode>=1.3.8,<2.0.0',
 'xebus-core-library>=1.4,<2.0',
 'xebus-sis-connector-core-library>=1.0,<2.0']

setup_kwargs = {
    'name': 'xebus-sis-connector-google-sheet',
    'version': '1.0.20',
    'description': "Connector to fetch data from a school's Eduka information system",
    'long_description': "# Xebus Google Sheet SIS Connector\nConnector to fetch family data from a school's Google Sheet document.\n\n## Google Service Account\n\nXebus Google Sheet SIS Connector needs to use the [service account `xebus-family-list-google-sheet@xebus-323504.iam.gserviceaccount.com`](https://console.cloud.google.com/iam-admin/serviceaccounts?project=xebus-323504&supportedpurview=project) to get access to the Google sheet that contains the families data of a school organization.\n\nA [service account](https://cloud.google.com/iam/docs/service-account-overview?_ga=2.62432492.-1545215353.1708747589) is a special kind of account typically used by an application, rather than a person. A service account is identified by its email address, which is unique to the account.  Applications use service accounts to make authorized API calls by authenticating as either the service account itself. When an application authenticates as a service account, it has access to all resources that the service account has permission to access.\n\n\n",
    'author': 'Daniel CAUNE',
    'author_email': 'daniel.caune@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xebus/xebus-sis-connector-google-sheet',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
