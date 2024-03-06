# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virtual_ecosystem',
 'virtual_ecosystem.core',
 'virtual_ecosystem.example_data',
 'virtual_ecosystem.example_data.generation_scripts',
 'virtual_ecosystem.models',
 'virtual_ecosystem.models.abiotic_simple',
 'virtual_ecosystem.models.animals',
 'virtual_ecosystem.models.hydrology',
 'virtual_ecosystem.models.litter',
 'virtual_ecosystem.models.plants',
 'virtual_ecosystem.models.soil']

package_data = \
{'': ['*'],
 'virtual_ecosystem.example_data': ['config/*',
                                    'data/*',
                                    'out/.gitignore',
                                    'source/*']}

install_requires = \
['Shapely>=1.8.4,<2.0.0',
 'dask>=2023.6.0,<2024.0.0',
 'dpath>=2.0.6,<3.0.0',
 'jsonschema>=4.14.0,<5.0.0',
 'netcdf4>=1.6.5,<2.0.0',
 'numpy>=1.23.0,<2.0.0',
 'pint>=0.20.1,<0.21.0',
 'scipy>=1.9.0,<2.0.0',
 'tomli-w>=1.0.0,<2.0.0',
 'tqdm>=4.66.2,<5.0.0',
 'xarray>=2024.02.0,<2025.0.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

entry_points = \
{'console_scripts': ['ve_run = virtual_ecosystem.entry_points:ve_run_cli']}

setup_kwargs = {
    'name': 'virtual-ecosystem',
    'version': '0.1.1a4',
    'description': 'An holistic ecosystem simulation model.',
    'long_description': '# Welcome to the Virtual Ecosystem\n\n[![codecov](https://codecov.io/gh/ImperialCollegeLondon/virtual_rainforest/branch/develop/graph/badge.svg)](https://codecov.io/gh/ImperialCollegeLondon/virtual_rainforest)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ImperialCollegeLondon/virtual_rainforest/develop.svg)](https://results.pre-commit.ci/latest/github/ImperialCollegeLondon/virtual_rainforest/develop)\n\nThis repository is the home for the development of the Virtual Ecosystem. The\nVirtual Ecosystem is a project to develop a simulation of all of the major\nprocesses involved in a real ecosystem including the:\n\n* growth and demographic processes of the primary producers within the forest,\n* microclimatic processes within and around the ecosystem,\n* hydrological processes within the canopy, soil and drainage networks,\n* biotic and abiotic processes within the soil, and the\n* growth and demography of heterotrophs.\n\n## Project details\n\nThis project is funded by a 2021 Distinguished Scientist award from the NOMIS\nFoundation to Professor Robert Ewers:\n\n* [NOMIS Award details](https://nomisfoundation.ch/people/robert-ewers/)\n* [NOMIS project summary](https://nomisfoundation.ch/research-projects/a-virtual-rainforest-for-understanding-the-stability-resilience-and-sustainability-of-complex-ecosystems/)\n\n<!-- markdownlint-disable-next-line  MD033 MD013-->\n[<img alt="NOMIS logo" src="https://github.com/ImperialCollegeLondon/virtual_ecosystem/blob/c94cef61d997764442d7beb9ac2eaedae71cfad1/docs/source/_static/images/logo-nomis-822-by-321.png?raw=true" width=250>](https://nomisfoundation.ch)\n\nThe research is based at Imperial College London:\n\n<!-- markdownlint-disable-next-line  MD033 MD013-->\n[<img alt="Imperial logo" src="https://github.com/ImperialCollegeLondon/virtual_ecosystem/blob/c94cef61d997764442d7beb9ac2eaedae71cfad1/docs/source/_static/images/IMP_ML_1CS_4CP_CLEAR-SPACE.png?raw=true" width=250>](https://imperial.ac.uk)\n\n## Project Team\n\n* Professor Robert Ewers\n* Olivia Daniel\n* Dr. Jaideep Joshi\n* Dr. David Orme\n* Dr. Vivienne Groner\n* Dr. Jacob Cook\n* Dr. Taran Rallings\n\nThe research team are supported by the Imperial College London\n[Research Software\nEngineering](https://www.imperial.ac.uk/admin-services/ict/self-service/research-support/rcs/service-offering/research-software-engineering/)\nteam.\n\n## Model documentation\n\nThe full documentation for the Virtual Ecosystem model can be viewed\n[here](https://virtual-ecosystem.readthedocs.io/en/latest/).\n',
    'author': 'Rob Ewers',
    'author_email': 'r.ewers@imperial.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://virtual-ecosystem.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
