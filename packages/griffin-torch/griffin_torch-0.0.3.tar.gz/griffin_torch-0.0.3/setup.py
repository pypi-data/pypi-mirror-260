# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['griffin_torch']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'griffin-torch',
    'version': '0.0.3',
    'description': 'Griffin - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Griffin\n\n## install\n`$ pip install griffin-torch`\n\n\n## usage\n```python\nimport torch\nfrom griffin_torch.main import Griffin\n\n# Forward pass\nx = torch.randint(0, 100, (1, 10))\n\n# Model\nmodel = Griffin(\n    dim=512,  # Dimension of the model\n    num_tokens=100,  # Number of tokens in the input\n    seq_len=10,  # Length of the input sequence\n    depth=8,  # Number of transformer blocks\n    mlp_mult=4,  # Multiplier for the hidden dimension in the MLPs\n    dropout=0.1,  # Dropout rate\n)\n\n# Forward pass\ny = model(x)\n\nprint(y)\n\n```\n\n\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/Griffin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
