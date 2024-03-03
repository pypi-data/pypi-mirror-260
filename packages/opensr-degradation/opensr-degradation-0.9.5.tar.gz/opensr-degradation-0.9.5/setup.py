# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensr_degradation', 'opensr_degradation.naipd']

package_data = \
{'': ['*'], 'opensr_degradation.naipd': ['models/*']}

install_requires = \
['numpy>=1.25.2',
 'pydantic>=2.6.3',
 'scikit-image>=0.19.3',
 'scipy>=1.11.4',
 'torch>=2.1.0',
 'torchvision>=0.16.0']

setup_kwargs = {
    'name': 'opensr-degradation',
    'version': '0.9.5',
    'description': 'A set of methods to emulate Sentinel-2 based on High-Resolution imagery',
    'long_description': '# opensr-degradation\n\n<div align="center">\n\n</div>\n\n## Install\n\n```python\npip install opensr-degradation\n```\n\n## Usage\n\n```python\nimport opensr_degradation\nimport torch\n\ndegradation_model = opensr_degradation.pipe(\n    sensor="naip_d",\n    add_noise=True,\n    params={\n        "method": [\n            "identity",\n            "gamma_lognormal",\n            "gamma_multivariate_normal",\n            "unet_histogram_matching",\n            "vae_histogram_matching",\n        ],\n        "device": "cuda",\n        "seed": 42,\n        "percentiles": [10, 25, 50, 75, 90],\n    },\n)\n\nimage = torch.rand(4, 256, 256)\nlr, hr = degradation_model(image)\n``` \n',
    'author': 'Cesar Aybar',
    'author_email': 'cesar.aybar@uv.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/csaybar/opensr-degradation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
