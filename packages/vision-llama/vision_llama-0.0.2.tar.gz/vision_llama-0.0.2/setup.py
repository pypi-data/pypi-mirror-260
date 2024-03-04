# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vision_llama']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'torch', 'torchvision', 'zetascale']

setup_kwargs = {
    'name': 'vision-llama',
    'version': '0.0.2',
    'description': 'Vision Llama - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Vision LLama\n\n\n\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/VisionLLaMA',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
