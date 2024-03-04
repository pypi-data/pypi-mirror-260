# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entropy_pooling']

package_data = \
{'': ['*']}

install_requires = \
['scipy>=1.10,<2.0']

setup_kwargs = {
    'name': 'entropy-pooling',
    'version': '1.0.2',
    'description': 'Entropy Pooling in Python with a BSD 3-Clause license.',
    'long_description': '[![pytest](https://github.com/fortitudo-tech/entropy-pooling/actions/workflows/tests.yml/badge.svg)](https://github.com/fortitudo-tech/entropy-pooling/actions/workflows/tests.yml)\n[![codecov](https://codecov.io/gh/fortitudo-tech/entropy-pooling/graph/badge.svg?token=XGIQ78ZLDN)](https://codecov.io/gh/fortitudo-tech/entropy-pooling)\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fortitudo-tech/entropy-pooling/HEAD?labpath=example)\n\nEntropy Pooling in Python\n=========================\n\nDue to popular demand from developers, this package contains the Entropy Pooling\nimplementation from the [fortitudo.tech Python package](https://github.com/fortitudo-tech/fortitudo.tech)\nwith a more permissive BSD 3-Clause license.\n\nThis package contains only one function called ep and has minimal dependencies\nwith just scipy. See [this example](https://github.com/fortitudo-tech/entropy-pooling/blob/main/example/EntropyPooling.ipynb)\nfor how you can import and use the ep function.\n\nYou can explore the example without local installations using\n[Binder](https://mybinder.org/v2/gh/fortitudo-tech/entropy-pooling/HEAD?labpath=example).\n\nInstallation instructions\n-------------------------\n\nInstallation can be done via pip:\n\n    pip install entropy-pooling\n\nTheory\n------\nEntropy Pooling is a powerful method for implementing subjective views and\nperforming stress-tests for fully general Monte Carlo distributions. It was first\nintroduced by [Meucci (2008)](https://ssrn.com/abstract=1213325) and refined\nwith sequential algorithms by [Vorobets (2021)](https://ssrn.com/abstract=3936392).\n\nThe original Entropy Pooling approach solves the minimum relative entropy problem\n\n$$q=\\underset{x}{\\text{argmin}}\\lbrace x^{T}\\left(\\ln x-\\ln p\\right)\\rbrace$$\n\nsubject to the constraints\n\n$$Gx\\leq h \\quad \\text{and} \\quad Ax=b.$$\n\nThe constraints matrices $A$ and $G$ contain transformations of the Monte Carlo\nsimulation that allow you to implement subjective views and stress-tests by\nchanging the joint scenario probabilities from a prior probability vector $p$\nto a posterior probability vector $q$.\n\nA useful statistic when working with Entropy Pooling is the effective number of\nscenarios introduced by [Meucci (2012)](https://ssrn.com/abstract=1971808). For\na causal Bayesian nets overlay on top of Entropy Pooling, see\n[Vorobets (2023)](https://ssrn.com/abstract=4444291).\n\nVideo walkthroughs\n------------------\n\nVideo walkthroughs of the two notebook examples for this package are available here\nhttps://youtu.be/hDt103zEML8 and here https://youtu.be/DK1Pv5tuLgo. The videos give\nadditional insights into the Entropy Pooling theory and its sequential refinements.\nIt is highly encouraged to watch these two quickly increase your understanding.',
    'author': 'Fortitudo Technologies',
    'author_email': 'software@fortitudo.tech',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://fortitudo.tech',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.13',
}


setup(**setup_kwargs)
